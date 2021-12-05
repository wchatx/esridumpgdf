import distutils.text_file
import os
import sys
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.install import install

VERSION = "0.0.3"


class VerifyVersionCommand(install):
    description = "verify that git tag matches VERSION prior to publishing to pypi"

    def run(self):
        tag = os.environ.get("GITHUB_REF")
        if not tag:
            info = "GITHUB_REF environment variable not available."
            sys.exit(info)

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


def parse_requirements(req):
    return distutils.text_file.TextFile(Path(__file__).with_name(req)).readlines()


with open(Path(__file__).with_name("README.md")) as f:
    long_description = f.read()

setup(
    name="esridumpgdf",
    version=VERSION,
    url="https://github.com/wchatx/esridumpgdf",
    license="MIT",
    packages=find_packages(exclude=("test*",)),
    author_email="wchatx@gmail.com",
    description="ArcGIS Map and Feature Services to GeoDataFrame",
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    install_requires=parse_requirements("requirements.txt"),
    cmdclass={
        "verify": VerifyVersionCommand,
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
