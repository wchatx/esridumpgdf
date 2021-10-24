from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from requests import Session
import pandas as pd


def server_info(url) -> pd.DataFrame:
    """

    index, layer_name, layer_number, service_name

    :param url:
    :return:
    """
    layers = []
    session = Session()
    resp = session.get(url, params=dict(f='json')).json()

    # get base services
    # for service in resp['services']:
    #     pass
    #
    #
    # # get folders
    # for folder in resp['folders']
    #
    # for folder in services.json()['folders']:
    #     print(f'Checking {folder}')
    #
    #     resp = requests.get(f'{BASE_URL}/{folder}', params=dict(f='pjson'))
    #     for service in resp.json()['services']:
    #         print(f'Checking {service["name"]}/{service["type"]}')
    #
    #         resp = requests.get(f'{BASE_URL}/{service["name"]}/{service["type"]}', params=dict(f='pjson'))
    #         for l in resp.json()['layers']:
    #             print(f'Checking layer {l["name"]}')
    #
    #             if service['type'] == 'MapServer':
    #                 url = f'{BASE_URL}/{service["name"]}/{service["type"]}/{l["id"]}'
    #                 print(f'Appending {url}')
    #                 extracts.append(url)





    def _get_layers(service):
        svc = session.get(service, params=dict(f='json')).json()
        lyrs = [x for x in svc['layers'] if 'layers' in svc]
        return lyrs

    with ThreadPoolExecutor(max_workers=cpu_count()) as pool:
        services = pool.map(
            lambda folder: [f'{url}/{service["name"]}/{service["type"]}' for service in
                            session.get(f'{url}/{folder}', params=dict(f='json')).json()['services']],
            resp['folders']
        )
        layers = pool.map(
            _get_layers,
            [item for sublist in services for item in sublist]
        )

    server = pd.DataFrame.from_records([item for sublist in layers for item in sublist])
    return server
