from concurrent.futures import ThreadPoolExecutor
from typing import List

from pandas import DataFrame

from ._base import Base


class Site(Base):
    def __init__(self, url: str):
        self.url = url
        super(Site, self).__init__(self.url)

    def _services(self) -> List[dict]:
        services = []
        if self.meta["services"]:
            services.extend(self.meta["services"])
        if self.meta["folders"]:
            for folder in self.meta["folders"]:
                response = self._session.get(f"{self.url}/{folder}").json()
                if "services" in response and response["services"]:
                    services.extend(response["services"])
        return [
            {**service, "url": f'{self.url}/{service["name"]}/{service["type"]}'}
            for service in services
        ]

    def services(self) -> DataFrame:
        """
        Get Site services

        :return: DataFrame of Site services
        """
        return DataFrame.from_records(self._services())

    def layers(self) -> DataFrame:
        """
        Get Site layers

        :return: DataFrame of Site layers
        """
        layers = []
        services = self._services()

        def _layers(service: dict):
            response = self._session.get(service["url"]).json()
            if "layers" in response:
                layers.extend(response["layers"])
            if "tables" in response:
                layers.extend(response["tables"])

        with ThreadPoolExecutor() as pool:
            pool.map(_layers, services)
        return DataFrame.from_records(layers)
