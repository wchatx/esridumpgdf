import os
import sys
from setuptools import setup, find_packages
import distutils.text_file
from pathlib import Path
from setuptools.command.install import install

VERSION = '0.0.3'


class VerifyVersionCommand(install):
    description = 'verify that git tag matches VERSION prior to publishing to pypi'

    def run(self):
        tag = os.getenv('GITHUB_REF').split('/')[-1]

        if tag != VERSION:
            info = 'Git tag: {0} does not match the version of this app: {1}'.format(
                tag, VERSION
            )
            sys.exit(info)


def parse_requirements(req):
    return distutils.text_file.TextFile(Path(__file__).with_name(req)).readlines()


with open(Path(__file__).with_name("README.md")) as f:
    long_description = f.read()

setup(
    name='esridumpgdf',
    version=VERSION,
    url='https://github.com/wchatx/esridumpgdf',
    license='MIT',
    packages=find_packages(exclude=('test*', )),
    author_email='wchatx@gmail.com',
    description='ArcGIS Map and Feature Services to GeoDataFrame',
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.6",
)
