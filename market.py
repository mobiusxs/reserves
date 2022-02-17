from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from evesso import Esi
# from dotenv import load_dotenv
import requests
import pandas as pd


# load_dotenv()

esi = Esi()
header = esi.header


def get_page_count(endpoint):
    response = requests.head(
        endpoint,
        headers=header
    )
    response.raise_for_status()
    return int(response.headers.get('X-Pages'))


def get_orders(endpoint, page_count):
    urls = [f"{endpoint}&page={i}" for i in range(1, page_count + 1)]

    session = FuturesSession()
    futures = [session.get(url, headers=header) for url in urls]

    orders = []
    for future in as_completed(futures):
        response = future.result()
        orders += response.json()
    return orders


def get_availability(structure_id):
    market_endpoint = f'https://esi.evetech.net/latest/markets/structures/{structure_id}/?datasource=tranquility'
    page_count = get_page_count(market_endpoint)
    orders = get_orders(market_endpoint, page_count)
    df = pd.DataFrame(orders)

    # get sell orders only
    df = df.loc[df['is_buy_order'] == False]

    # remove unrelated columns
    df = df[['type_id', 'volume_remain']]

    # group all same-type orders, summing remaining volume
    df = df.groupby(by=["type_id"]).sum()
    return df.to_dict().get('volume_remain')


if __name__ == '__main__':
    print(get_availability(1035466617946))
