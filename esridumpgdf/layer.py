from pandas import to_datetime
from geopandas import GeoDataFrame
from esridump.dumper import EsriDumper

from .base import Base


class Layer(Base):
    def __init__(self, url: str, **kwargs):
        super(Layer, self).__init__(url, **kwargs)

    def to_gdf(self, **kwargs) -> GeoDataFrame:
        crs = kwargs.get('crs') or 4326
        layer = EsriDumper(self.url, outSR=crs, **kwargs)

        if self.meta['type'] == 'Group Layer':
            raise Exception('Provided URL is a Group Layer. This is currently unsupported')

        gdf = GeoDataFrame.from_features(features=layer, crs=crs)
        for field in self.meta['fields']:
            if field['type'] == 'esriFieldTypeOID':
                gdf.set_index(field['name'], inplace=True)
            if field['type'] == 'esriFieldTypeDate':
                gdf[field['name']] = to_datetime(gdf[field['name']], unit='ms')
            if field['type'] == 'esriFieldTypeInteger':
                gdf[field['name']] = gdf[field['name']].astype('Int64')
        return gdf
