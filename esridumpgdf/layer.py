from typing import Dict, Union

from esridump.dumper import EsriDumper
from geopandas import GeoDataFrame
from pandas import to_datetime

from ._base import Base


class Layer(Base):
    def __init__(self, url: str, **kwargs):
        super(Layer, self).__init__(url)
        self.crs = kwargs.get("crs") or 4326
        self.layer = EsriDumper(self.url, outSR=str(self.crs), **kwargs)

    def to_gdf(
        self, columns: list = None
    ) -> Union[GeoDataFrame, Dict[str, GeoDataFrame]]:
        """
        Export an ArcGIS Server layer to GeoDataFrame

        :param columns: list of column names, optional
            Optionally specify the column names to include in the output frame.
            This does not overwrite the property names of the input, but can
            ensure a consistent output format.
        :return:
        """
        gdf = GeoDataFrame.from_features(
            features=self.layer, crs=self.crs, columns=columns
        )
        for field in self.meta["fields"]:
            if field["type"] == "esriFieldTypeOID":
                gdf.set_index(field["name"], inplace=True)
            if field["type"] == "esriFieldTypeDate":
                gdf[field["name"]] = to_datetime(gdf[field["name"]], unit="ms")
            if field["type"] == "esriFieldTypeInteger":
                gdf[field["name"]] = gdf[field["name"]].astype("Int64")
        return gdf
