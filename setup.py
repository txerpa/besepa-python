#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

from besepasdk.config import __version__

long_description = """
    The Besepa SDK provides Python APIs to create, process and manage SEPA direct debits.

    1. https://github.com/txerpa/Besepa-Python-SDK - README and Samples
    2. http://docs.besepaen.apiary.io - API Reference
  """

setup(
  name='besepasdk',
  version=__version__,
  author='Mateu Cànaves',
  author_email='mateu.canavces@gmail.com',
  packages=['besepasdk'],
  scripts=[],
  url='https://github.com/txerpa/Besepa-Python-SDK',
  license='MIT',
  description='The Besepa SDK provides Python APIs to create, process and manage SEPA direct debits.',
  long_description=long_description,
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['besepa', 'rest', 'sdk', 'debits', 'sepa']
)
