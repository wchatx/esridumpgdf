# esridumpgdf

Simple functions using [pyesridump](https://github.com/openaddresses/pyesridump) 
and [geopandas](https://github.com/geopandas/geopandas) to create GeoDataFrames.  

## Install
```
pip install git+https://github.com/wchatx/esridumpgdf.git
```

## Usage
For exporting a single Map or Feature service to GeoDataFrame:
```python
from esridumpgdf import Layer
layer = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/911CallsHotspot/MapServer/1'
gdf = Layer(layer).to_gdf()
```

To export an entire service to a multiple GeoDataFrames:
```python
from esridumpgdf import Service
service = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Wildfire/MapServer'
gdfs = Service(service).to_gdfs()
```