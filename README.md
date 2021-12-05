# esridumpgdf

[![CI](https://github.com/wchatx/esridumpgdf/actions/workflows/test.yml/badge.svg)](https://github.com/wchatx/esridumpgdf/actions/workflows/test.yml)

Export ArcGIS Map and Feature services and layers to GeoDataFrame  using [pyesridump](https://github.com/openaddresses/pyesridump) 
and [geopandas](https://github.com/geopandas/geopandas).

## Install
```
pip install esridumpgdf
```

## Usage
For exporting a single layer to GeoDataFrame:
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

Write the service to geopackage. Each layer (and optionally table) will be available as a layer in the geopackage
```python
from esridumpgdf import Service
service = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Wildfire/MapServer'
gpkg = Service(service).to_gpkg(
    filename='wildfire.gpkg', include_tables=True
)
```

Get a dataframe of all the services and layers available on the entire ArcGIS Server site
```python
from esridumpgdf import Site
site = Site('https://sampleserver6.arcgisonline.com/arcgis/rest/services')
services = site.services()
layers = site.layers()
```

See the example notebook for more methods

## Developing
This project uses poetry and pre-commit. Ensure these are available  

Clone the repo, run `poetry install` and `pre-commit install`  

To bump versions, run `make version RULE=<rule>` where `rule` is a valid value from `poetry version`.