from esridumpgdf import layer_to_gdf


def test_layer_to_gdf():
    layer = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/911CallsHotspot/MapServer/1'
    gdf = layer_to_gdf(layer)

    assert gdf.shape[0]
    assert gdf.index.name == 'FID'


if __name__ == '__main__':
    test_layer_to_gdf()
