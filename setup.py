# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages


setup(
	name="setuptools_extversion",
	version="0.0.0",
	author="Marc Abramowitz",
	author_email="marc@marc-abramowitz.com",
	url="https://github.com/msabramo/python_setuptools_extversion/",
	description="Adds an `extversion` param to setup that can be a callable",
	long_description="",
	license="MIT",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Topic :: Software Development :: Version Control",
		"Framework :: Setuptools Plugin",
	],
	packages=find_packages(),
	entry_points = {
		"distutils.setup_keywords": [
			"extversion = setuptools_extversion:version_calc",
		],
	},
)
