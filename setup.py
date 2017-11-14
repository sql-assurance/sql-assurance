#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'thrift==0.9.3',
    'avro==1.8.1',
    'impyla',
    'PyYaml',
    'celery',
    'numpy',
    'termcolor',
    'unittest2'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='sql_assurance',
    version='0.0.1',
    description="Audit your databases",
    long_description=readme + '\n\n' + history,
    author="Sergio Sola",
    author_email='introduccio@gmail.com',
    url='https://github.com/ssola/sql_assurance',
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='sql_assurance',
        entry_points={
        'console_scripts': [
            'sql-assurance = sql_assurance.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
