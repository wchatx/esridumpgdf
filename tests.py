from collections import OrderedDict

from esridumpgdf import Layer, Service, Site

service = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/ServiceRequest/MapServer"
layer = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/911CallsHotspot/MapServer/1"


def test_layer_to_gdf():
    gdf = Layer(layer).to_gdf()
    assert gdf.shape[0]
    assert gdf.index.name == "FID"
    assert gdf.geometry.name == "geometry"


# def test_group_layer_to_gdfs():
#     layer = "https://sampleserver6.arcgisonline.com/arcgis/rest/services/Water_Network/MapServer/1"
#     gdf = Layer(layer).to_gdf()
#
#     assert len(list(gdf.keys())) == 3


def test_service_to_gdfs():
    gdfs = Service(service).to_gdfs()
    assert gdfs
    assert isinstance(gdfs, list)


def test_service_with_table():
    gdfs = Service(service).to_gdfs()
    assert gdfs
