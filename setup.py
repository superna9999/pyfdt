#!/usr/bin/env python

from distutils.core import setup

setup(name='pyfdt',
      version='1.0',
      description='Python Flattened Device Tree Library',
      author='Neil \'Superna\' Armstrong',
      author_email='superna9999@gmail.com',
      url='https://github.com/superna9999/pyfdt',
      packages=['pyfdt'],
      scripts=['dtbdump.py'],
     )
