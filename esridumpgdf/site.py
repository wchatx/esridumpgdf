from typing import List, Dict

from .base import Base
from .service import Service
import geopandas as gpd


class Site(Base):
    def __init__(self, url: str, **kwargs):
        super(Site, self).__init__(url, **kwargs)
        self.current_version = self.meta['currentVersion']

        # if list(self.meta.keys()) != ['currentVersion', 'folders', 'services']:
        #     raise Exception('Provided URL was not an ArcGIS Server site')

    def __repr__(self) -> str:
        return f'Site(url={self.url}, currentVersion={self.meta["currentVersion"]})'

    def _repr_html_(self) -> str:
        df = gpd.GeoDataFrame({'currentVersion': [self.meta['currentVersion']], 'url': [self.url]})
        return df.to_html()

    @property
    def version(self) -> float:
        return self.current_version

    def services(self) -> gpd.GeoDataFrame:
        _services: List[Service] = []

        for folder in self.meta['folders']:
            services = self.session.get(f'{self.url}/{folder}', params=dict(f='json')).json()['services']
            for service in services:
                if service['type'] in ['MapServer', 'FeatureServer']:
                    service = Service(f'{self.url}/{service["name"]}/{service["type"]}')
                    _services.append(service.meta)

        return gpd.GeoDataFrame.from_records(_services)

    def layers(self) -> gpd.GeoDataFrame:
        _layers: List[Dict] = []
        return gpd.GeoDataFrame.from_records(_layers)

    def tables(self) -> gpd.GeoDataFrame:
        _tables: List[Dict] = []
        return gpd.GeoDataFrame.from_records(_tables)
