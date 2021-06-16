#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

  setuptools.setup(name='rfslib',
    version='0.3.2',
    description='Remote file system libraries for data manipulation between remote /and local host/ (cp, mv, ls, rm,..)',
    long_description=long_description,
    author='Přemysl Šťastný',
    author_email='p-w@stty.cz',
    url='https://git.profinit.eu/pstastny/rfslib',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
      'pysmb>=1.2.7,<2',
      'paramiko>=2.7.2,<3'
    ]
  )
