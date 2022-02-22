import sqlite3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

import requests
import pandas as pd
from evesso import Esi
from dotenv import load_dotenv

from core import config

load_dotenv(config.ENV_PATH)

esi = Esi(jwt_file_path=config.JWT_FILE_PATH)
header = esi.header


def get_page_count(endpoint: str) -> int:
    """Make a head request to the market endpoint
    to get the total number of order pages.

    :param endpoint: str parameterized ESI endpoint to make head request to
    :return: int number of order pages
    """

    response = requests.head(
        endpoint,
        headers=header
    )
    response.raise_for_status()
    return int(response.headers.get('X-Pages'))


def get_orders(endpoint: str, page_count: int):
    """Concurrently request all order pages from the market using
    the provided parameterized ESI endpoint. The base endpoint URL
    string will have the page argument appended to the query string.

    :param endpoint: str parameterized ESI endpoint to make get request to
    :param page_count: int number of order pages
    :return: list[dict] all orders currently on the market
    """

    urls = [f"{endpoint}&page={i}" for i in range(1, page_count + 1)]

    session = FuturesSession()
    futures = [session.get(url, headers=header) for url in urls]

    orders = []
    for future in as_completed(futures):
        response = future.result()
        orders += response.json()
    return orders


def compress_orders(orders):
    """Compress all market orders down to only the relevant values
    of relevant orders. All orders for like types are grouped.
    Volume is the sum of all orders for a type, and price is the
    current lowest sell price.

    :param orders: list[dict] all orders currently on the market
    :return: list[tuple] type_id, price, and volume of all types on the market
    """

    df = pd.DataFrame(orders)

    # remove buy orders
    df = df.loc[df['is_buy_order'] == False]

    # remove unrelated columns
    df = df[['type_id', 'price', 'volume_remain']]

    # Group all orders for the same type. Find lowest price, and total volume
    df = df.groupby(['type_id']).agg({'price': 'min', 'volume_remain': 'sum'})

    # return list of tuples: [(type_id, price, volume_remain)]
    return df.to_records()


def insert_into_db(orders) -> None:
    """Iterate over all order tuples in the list and
    update the values in the database with the tuple data.

    :param orders: list[tuple] type_id, price, and volume of all types on the market
    :return: None
    """

    conn = sqlite3.connect(config.DATABASE_PATH)
    c = conn.cursor()

    for order in orders:
        type_id, price, volume = order
        c.execute("""UPDATE item SET price=?, available=? WHERE id=?""", (float(price), int(volume), int(type_id)))
    conn.commit()
    c.close()
    conn.close()


def main() -> None:
    """Retrieve current market orders and load price and volume data into database"""

    market_endpoint = f'https://esi.evetech.net/latest/markets/structures/1035466617946/?datasource=tranquility'
    page_count = get_page_count(market_endpoint)
    all_orders = get_orders(market_endpoint, page_count)
    orders = compress_orders(all_orders)
    insert_into_db(orders)


if __name__ == '__main__':
    main()
