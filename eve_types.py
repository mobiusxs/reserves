import bz2
from io import BytesIO

import pandas as pd
import requests

CSV_PATH = 'data/types.csv'


def download_types():
    """Download the BZ2 compressed invTypes.csv file located at
    https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2.
    Decompress the file contents, remove all columns except
    the typeID and typeName columns, and write the csv to disk.
    """

    response = requests.get('https://www.fuzzwork.co.uk/dump/latest/invTypes.csv.bz2')
    response.raise_for_status()
    content = bz2.decompress(response.content)
    df = pd.read_csv(BytesIO(content))
    df = df[['typeID', 'typeName']]
    df.to_csv(CSV_PATH, encoding='utf-8', index=False)


def get_id_dict() -> dict:
    """Return a dictionary where the keys are typeIDs and the values are typeNames

    Example:
        {
            0: '#System',
            1: 'Corporation',
            2: 'Region',
            3: 'Constellation',
            4: 'Solar System',
            5: 'Sun G5 (Yellow)',
            6: 'Sun K7 (Orange)'
        }

    :return: dict a typeID to typeName mapping
    """

    df = pd.read_csv(CSV_PATH)
    return dict(zip(df.typeID, df.typeName))


def get_name_dict() -> dict:
    """Return a dictionary where the keys are typeIDs and the values are typeNames

    Example:
        {
            '#System': 0,
            'Corporation': 2,
            'Region': 3,
            'Constellation': 4,
            'Solar System': 5,
            Sun G5 (Yellow)': 6,
            'Sun K7 (Orange)': 7
        }

    :return: dict a typeName to typeID mapping
    """

    df = pd.read_csv(CSV_PATH)
    return dict(zip(df.typeName, df.typeID))


if __name__ == '__main__':
    download_types()
