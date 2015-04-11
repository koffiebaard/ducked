#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Ducked',
    version='0.7',
    description='Simple app launcher that doesn\'t suck (yet)',
    author='Wisc',
    author_email='wisc.whut@gmail.com',
    url='https://github.com/wisc/ducked',
    scripts=['ducked.py'],
    package_dir = {'': '.'},
    packages = find_packages() # ['src/ext', 'src/gui', 'src/lib', 'src/models'],
)