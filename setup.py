from setuptools import setup
import distutils.text_file
from pathlib import Path


def parse_requirements(req):
    return distutils.text_file.TextFile(Path(__file__).with_name(req)).readlines()


with open(Path(__file__).with_name("README.md")) as f:
    long_description = f.read()

setup(
    name='esridump-gdf',
    version='0.0.1',
    url='https://github.com/wchatx/esridump-gdf',
    license='MIT',
    author='Cole Howard',
    author_email='wchatx@gmail.com',
    description='ArcGIS Map and Feature Services to GeoDataFrame',
    use_scm_version=True,
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.6",
)
