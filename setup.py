# -*- coding: utf-8 -*-
import os
from setuptools import setup

# Get contents of README for long description
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file) as f:
    README = f.read()

setup(
    name="bng",
    version="1.0.2",
    description=("Convert between BNG grid refs (e.g. NT123456) and "
                 "OSGB36 (EPSG:27700) coords"),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/volcan01010/bng",
    author="Dr John A Stevenson",
    author_email="johnalexanderstevenson@gmail.com",
    license="GPLv3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
    ],
    py_modules=["bng"]
)
