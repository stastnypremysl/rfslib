#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='rfslib',
      version='0.1.0.0',
      description='Remote file system libraries for data manipulation between remote /and local host/ (cp, mv, ls, rm,..)',
      author='Přemysl Šťastný',
      author_email='p-w@stty.cz',
      url='https://git.profinit.eu/pstastny/rfslib',
      packages=find_packages(include=['rfslib', 'rfslib.*'])
     )
