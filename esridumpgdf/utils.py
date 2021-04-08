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

    def _get_layers(service):
        svc = session.get(service, params=dict(f='json')).json()
        if 'layers' in svc:
            for layer in svc['layers']:
                
        return svc

    with ThreadPoolExecutor(max_workers=cpu_count()) as pool:
        services = pool.map(
            lambda folder: [f'{url}/{service["name"]}/{service["type"]}' for service in
                            session.get(f'{url}/{folder}', params=dict(f='json')).json()['services']],
            resp['folders'])
        layers = pool.map(
            _get_layers,
            [item for sublist in services for item in sublist]
        )

    server = pd.DataFrame.from_records([item for sublist in layers for item in sublist])
    return server
