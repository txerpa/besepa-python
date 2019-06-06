import os
import re
import codecs

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = codecs.open(os.path.join(package, '__init__.py'), encoding='utf-8').read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


setup(
    name='besepa',
    version=get_version('besepa'),
    author='Mateu Cànaves',
    author_email='mateu.canaves@gmail.com',
    maintainer='Biel Massot',
    maintainer_email='biel.massot@txerpa.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/txerpa/besepa-python',
    license='MIT',
    description="Simple python wrapper to Besepa.com's API.",
    long_description="""
        The Besepa Python provides simple python wrapper to Besepa.com's API.
        
        1. https://github.com/txerpa/besepa-python - README and Samples
        2. http://docs.besepaen.apiary.io - API Reference
    """,
    install_requires=[
        'requests>=2.22.0,<3.0'
    ],
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
