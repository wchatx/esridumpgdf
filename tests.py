from typing import OrderedDict

from esridumpgdf import Layer, Service


def test_layer_to_gdf():
    layer = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/911CallsHotspot/MapServer/1'
    gdf = Layer(layer).to_gdf()

    assert gdf.shape[0]
    assert gdf.index.name == 'FID'
    assert gdf.geometry.name == 'geometry'


def test_service_to_gdfs():
    service = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Wildfire/MapServer'
    gdfs = Service(service).to_gdfs()

    assert gdfs
    assert isinstance(gdfs, OrderedDict)

