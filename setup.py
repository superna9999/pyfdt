#!/usr/bin/env python

from setuptools import setup

setup(name='pyfdt',
      version='0.3',
      description='Python Flattened Device Tree Library',
      author='Neil \'Superna\' Armstrong',
      author_email='superna9999@gmail.com',
      url='https://github.com/superna9999/pyfdt',
      packages=['pyfdt'],
      scripts=['dtbdump.py', 'fdtmerge.py',  'jsonfdtdump.py'],
     )
