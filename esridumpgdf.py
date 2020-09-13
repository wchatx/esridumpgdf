from pandas import to_datetime
from geopandas import GeoDataFrame
from esridump.dumper import EsriDumper


def layer_to_gdf(url: str, crs: int = 4326, **kwargs) -> GeoDataFrame:
    """
    Export an ArcGIS Server Map or Feature service to GeoDataFrame

    :param url:
    :param crs:
    :return:
    """
    layer = EsriDumper(url, outSR=crs, **kwargs)
    gdf = GeoDataFrame.from_features(features=layer, crs=crs)
    for field in layer.get_metadata()['fields']:
        if field['type'] == 'esriFieldTypeOID':
            gdf.set_index(field['name'], inplace=True)
        if field['type'] == 'esriFieldTypeDate':
            gdf[field['name']] = to_datetime(gdf[field['name']], unit='ms')
    return gdf
