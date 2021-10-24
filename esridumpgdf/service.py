import os
import shutil
from collections import OrderedDict
from typing import List, Dict, Union

from pandas import Series
from geopandas import GeoDataFrame

from .base import Base
from .layer import Layer


class Service(Base):
    # mapName
    name: str
    description: str = None
    # copyrightText
    copyright_text: str = None
    # supportsDynamicLayers
    supports_dynamic_layers: bool
    # spatialReference
    spatial_reference: dict

    def __init__(self, url: Union[str], **kwargs):
        super(Service, self).__init__(url, **kwargs)

    @property
    def tables(self) -> GeoDataFrame:
        return GeoDataFrame(data=self.meta['tables'])

    @property
    def layers(self) -> GeoDataFrame:
        _layers = [{**layer, 'url': f'{self.url}/{layer["id"]}'} for layer in self.meta['layers']]
        return GeoDataFrame(data=_layers)

    def to_gpkg(self, path: str, include_tables: bool = True, overwrite: bool = False, **kwargs) -> None:
        """
        Export service to geopackage

        :return:
        """
        if os.path.exists(path):
            if overwrite:
                shutil.rmtree(path)
            else:
                raise Exception('Output path exists and overwrite is False')
        self.layers.apply(
            lambda layer: Layer(layer.url, **kwargs).to_gdf().to_file(
                filename=f'{path}.gpkg', driver='GPKG', index=True, layer=layer['name']
            ),
            axis=1
        )
        return

    def to_gdfs(self, include_tables: bool = True, **kwargs) -> Dict[str, GeoDataFrame]:
        """
        Export a complete ArcGIS Server Map or Feature service to GeoDataFrames

        :param include_tables: whether to include attribute-only tables
        :param kwargs: extra keyword arguments provided to pyesridump's EsriDumper class
        :return:
        """
        layers = self.layers[self.layers.type == 'Feature Layer']
        gdfs = layers.apply(lambda x: Layer(x['url']), axis=1)
        # gdfs = OrderedDict(
        #     {layer['id']: Layer(f'{self.url}/{layer["id"]}', **kwargs).to_gdf()
        #      for layer in sorted(layers, key=lambda _: _['id'])}
        # )
        # if self.tables and include_tables:
        #     gdfs.update({table['name']: Layer(f'{self.url}/{table["id"]}').to_gdf() for table in self.tables})
        return gdfs
