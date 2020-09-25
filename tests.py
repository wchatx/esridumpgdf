from collections import OrderedDict

from esridumpgdf import Layer, Service


def test_layer_to_gdf():
    layer = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/911CallsHotspot/MapServer/1'
    gdf = Layer(layer).to_gdf()

    assert gdf.shape[0]
    assert gdf.index.name == 'FID'
    assert gdf.geometry.name == 'geometry'


def test_group_layer_to_gdfs():
    layer = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Water_Network/MapServer/1'
    gdf = Layer(layer).to_gdf()

    assert len(list(gdf.keys())) == 3


def test_service_to_gdfs():
    service = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Wildfire/MapServer'
    gdfs = Service(service).to_gdfs()

    assert gdfs
    assert isinstance(gdfs, OrderedDict)


def test_service_with_table():
    service = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/ServiceRequest/MapServer'
    gdfs = Service(service).to_gdfs()

    assert gdfs

