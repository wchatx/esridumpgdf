from pandas import to_datetime
from geopandas import GeoDataFrame
from esridump.dumper import EsriDumper


def layer_to_gdf(url: str, **kwargs) -> GeoDataFrame:
    """
    Export an ArcGIS Server Map or Feature service to GeoDataFrame

    ::
        from esridumpgdf import layer_to_gdf
        layer = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/911CallsHotspot/MapServer/1'
        gdf = layer_to_gdf(layer)

    :param url: url of the esri layer
    :return: GeoDataFrame
    """
    crs = kwargs.get('crs') or 4326
    layer = EsriDumper(url, outSR=crs, **kwargs)
    gdf = GeoDataFrame.from_features(features=layer, crs=crs)
    for field in layer.get_metadata()['fields']:
        if field['type'] == 'esriFieldTypeOID':
            gdf.set_index(field['name'], inplace=True)
        if field['type'] == 'esriFieldTypeDate':
            gdf[field['name']] = to_datetime(gdf[field['name']], unit='ms')
    return gdf
