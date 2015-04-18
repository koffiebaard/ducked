#!/usr/bin/env python

import os
import json
from setuptools import setup, find_packages


# Load app meta info
meta_json = open(os.path.dirname(os.path.realpath(__file__)) + "/meta.json", "r")
app = json.load(meta_json)

setup(
    name=app["name"],
    version=app["version"],
    description=app["description"],
    author=app["author"],
    author_email=app["author_email"],
    url=app["url"],
    scripts=['ducked.py'],
    package_dir = {'': '.'},
    packages = find_packages() # ['src/ext', 'src/gui', 'src/lib', 'src/models'],
)