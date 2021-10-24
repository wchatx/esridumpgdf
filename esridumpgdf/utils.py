from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from requests import Session
import pandas as pd
import geopandas as gpd


def server_info(url) -> pd.DataFrame:
    """

    :param url:
    :return:
    """
    session = Session()
    resp = session.get(url, params=dict(f='json')).json()
    services = gpd.GeoDataFrame()
    layers = gpd.GeoDataFrame()

    with ThreadPoolExecutor(max_workers=cpu_count()) as pool:
        services = pool.map(
            lambda folder: [f'{url}/{service["name"]}/{service["type"]}' for service in
                            session.get(f'{url}/{folder}', params=dict(f='json')).json()['services']],
            resp['folders'])
        layers = pool.map(
            lambda service: print({k: v for k, v in session.get(service, params=dict(f='json')).json().items()}),
            [item for sublist in services for item in sublist]
        )

    server = pd.DataFrame.from_records([item for sublist in layers for item in sublist])
    return server

