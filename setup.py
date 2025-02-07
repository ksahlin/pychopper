#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from glob import glob

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'parasail',
    'biopython',
    'matplotlib',
    'six',
    'tqdm',
    'pandas',
    'pytest'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pychopper',
    version='0.6.1',
    description="TODO.",
    long_description=readme,
    author="ONT Applications Group",
    author_email='Apps@nanoporetech.com',
    url='',
    packages=[
        'pychopper',
    ],
    package_dir={'pychopper':
                 'pychopper'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='pychopper',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
    ],
    tests_require=test_requirements,
    scripts=[x for x in glob('scripts/*.py') if x != 'scripts/__init__.py']
)
