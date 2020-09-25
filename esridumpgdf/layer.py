from typing import Union, Dict
from collections import OrderedDict

from pandas import to_datetime
from geopandas import GeoDataFrame
from esridump.dumper import EsriDumper

from .base import Base


class Layer(Base):
    def __init__(self, url: str, **kwargs):
        super(Layer, self).__init__(url, **kwargs)

    @property
    def type(self) -> str:
        return self.meta['type']

    def to_gdf(self, **kwargs) -> Union[GeoDataFrame, Dict[str, GeoDataFrame]]:
        """
        Export layer to GeoDataFrame

        :param kwargs: extra keyword arguments provided to pyesridump's EsriDumper class
        :return:
        """
        crs = kwargs.get('crs') or 4326
        layer = EsriDumper(self.url, outSR=crs, **kwargs)

        if self.type == 'Group Layer':
            gdfs = OrderedDict(
                {layer['name']: Layer(f'{"/".join(self.url.split("/")[:-1])}/{layer["id"]}', **kwargs).to_gdf()
                 for layer in self.meta['subLayers']}
            )
            return gdfs

        gdf = GeoDataFrame.from_features(features=layer, crs=crs)
        for field in self.meta['fields']:
            if field['type'] == 'esriFieldTypeOID':
                gdf.set_index(field['name'], inplace=True)
            if field['type'] == 'esriFieldTypeDate':
                gdf[field['name']] = to_datetime(gdf[field['name']], unit='ms')
            if field['type'] == 'esriFieldTypeInteger':
                gdf[field['name']] = gdf[field['name']].astype('Int64')
        return gdf
