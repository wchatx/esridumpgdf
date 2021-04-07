from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from requests import Session
import pandas as pd


def server_info(url) -> pd.DataFrame:
    """

    :param url:
    :return:
    """
    session = Session()
    resp = session.get(url, params=dict(f='json')).json()

    def _get(x):
        resp = session.get(f'{url}/{x}', params=dict(f='json')).json()
        services = [f'{url}{y["name"]}/{y["type"]}' for y in resp['services']]
        layers = [session.get(t, params=dict(f='json')).json() for t in services]
        return layers

    with ThreadPoolExecutor(max_workers=cpu_count()) as pool:
        r = pool.map(_get, resp['folders'])

    layers = []
    for folder in r:
        [[layers.append(y) for y in x['layers']] for x in folder]
    print(len(layers))
    server = pd.DataFrame.from_records(layers)
    return server
