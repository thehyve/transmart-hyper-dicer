#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

if sys.version_info < (3, 6):
    sys.exit(
        'Python < 3.6 is not supported. You are using Python {}.{}.'.format(
            sys.version_info[0], sys.version_info[1])
    )

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit dicer/__version__.py
version = {}
with open(os.path.join(here, 'dicer', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt', 'r') as f:
    required_packages = f.read().splitlines()

setup(
    name='transmart-hyper-dicer',
    version=version['__version__'],
    description='Data slicing tool for reading data from one tranSMART and uploading it to another',
    long_description=readme + '\n\n',
    author='Ewelina Grudzien',
    author_email='ewelina@thehyve.nl',
    url='https://github.com/thehyve/transmart-hyper-dicer',
    packages=[
        'dicer',
        'dicer.mappers'
    ],
    entry_points={
        'console_scripts': ['transmart-hyper-dicer=dicer.main:main'],
    },
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords=[
        'transmart-hyper-dicer',
        'transmart'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    python_requires='>=3.6.0',
    install_requires=required_packages,
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark',
        # dependency for `python setup.py bdist_wheel`
        'wheel'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
        'responses'
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'pygments', 'yapf', 'isort'],
    }
)
