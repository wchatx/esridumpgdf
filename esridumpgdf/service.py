from typing import Dict, Optional

from geopandas import GeoDataFrame
from pandas import DataFrame, concat

from ._base import Base
from .layer import Layer


class Service(Base):
    def __init__(self, url):
        self.url = url
        super(Service, self).__init__(self.url)

    def layers(self, include_tables: bool = True) -> DataFrame:
        """
        Get Service layers.

        Args:
            include_tables: include Service tables

        Returns:

        """
        layers = DataFrame(
            data=[
                {**layer, "url": f'{self.url}/{layer["id"]}'}
                for layer in self.meta["layers"]
            ]
        )
        layers.set_index("id", inplace=True)

        if include_tables and self.meta["tables"]:
            tables = DataFrame(
                data=[
                    {**table, "url": f'{self.url}/{table["id"]}'}
                    for table in self.meta["tables"]
                ]
            )
            tables.set_index("id", inplace=True)
            layers = concat([layers, tables])

        return layers

    def to_gpkg(
        self,
        filename: str,
        index: bool = True,
        schema: Optional[dict] = None,
        include_tables: bool = True,
        **kwargs,
    ) -> str:
        """
        Export an ArcGIS Server Map or Feature service to geopackage

        Args:
            filename: File path or file handle to write to.
            index: If True, write index into one or more columns (for MultiIndex).
                Default None writes the index into one or more columns only if
                the index is named, is a MultiIndex, or has a non-integer data
                type. If False, no index is written.
            schema: If specified, the schema dictionary is passed to Fiona to
                better control how the file is written.
            include_tables: include Service tables
            **kwargs: extra keyword arguments provided to the EsriDumper class

        Returns:

        """
        layers = self.layers(include_tables).to_dict(orient="records")
        for layer in layers:
            if layer["type"] in self._SUPPORTED_TYPES:
                Layer(layer["url"], **kwargs).to_gdf().to_file(
                    filename,
                    driver="GPKG",
                    index=index,
                    schema=schema,
                    layer=layer["name"],
                )
        return filename

    def to_gdfs(self, include_tables: bool = True, **kwargs) -> Dict[str, GeoDataFrame]:
        """
        Export an ArcGIS Server Map or Feature service to GeoDataFrames

        Args:
            include_tables: include Service tables
            **kwargs: extra keyword arguments provided to the EsriDumper class

        Returns: dict with layer numbers and layer GeoDataFrames

        """
        layers = self.layers(include_tables).to_dict(orient="records")
        output = {
            layer["id"]: Layer(layer["url"], **kwargs).to_gdf() for layer in layers
        }
        return output
