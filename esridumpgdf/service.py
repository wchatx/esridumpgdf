from collections import OrderedDict
from typing import List, Dict

from geopandas import GeoDataFrame

from .base import Base
from .layer import Layer


class Service(Base):
    def __init__(self, url, **kwargs):
        super(Service, self).__init__(url, **kwargs)

    @property
    def layers(self) -> List[dict]:
        return self.meta['layers']

    @property
    def tables(self) -> List[dict]:
        return self.meta['tables']

    def to_gdfs(self, include_tables: bool = True, **kwargs) -> Dict[str, GeoDataFrame]:
        """
        Export a complete ArcGIS Server Map or Feature service to GeoDataFrames

        :param include_tables: whether to include attribute-only tables
        :param kwargs: extra keyword arguments provided to pyesridump's EsriDumper class
        :return:
        """
        layers = [layer for layer in self.layers if layer['type'] != 'Group Layer']
        gdfs = OrderedDict(
            {layer['name']: Layer(f'{self.url}/{layer["id"]}', **kwargs).to_gdf()
             for layer in sorted(layers, key=lambda _: _['name'])}
        )
        if self.tables and include_tables:
            gdfs.update({table['name']: Layer(f'{self.url}/{table["id"]}').to_gdf() for table in self.tables})
        return gdfs
