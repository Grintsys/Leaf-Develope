# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in leaf_develop/__init__.py
from leaf_develop import __version__ as version

setup(
	name='leaf_develop',
	version=version,
	description='This app contain all modules of leaf',
	author='Frappe',
	author_email='info@grintsys.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
