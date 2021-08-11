#!/usr/bin/env python3

import setuptools


with open("README.md", "r", encoding="utf-8") as freadme, open("version.txt", "r") as fversion:
  long_description = freadme.read()
  version = fversion.read().splitlines()[0]

  setuptools.setup(name='rfslib',
    version=version,
    description='Remote file system libraries for data manipulation between remote /and local host/ (cp, mv, ls, rm,..)',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Přemysl Šťastný',
    author_email='p-w@stty.cz',
    url='https://git.profinit.eu/pstastny/rfslib',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
      'pysmb>=1.2.7,<2',
      'paramiko>=2.7.2,<3',
      'smbprotocol>=1.6.1,<2',
      'ftputil>=5.0.1,<6'
    ]
  )
