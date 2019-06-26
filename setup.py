#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Zabbix Tuner
"""
import os
from setuptools import setup, find_packages, findall


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Zabbix Tuner',
    url='https://github.com/janssenlima/ZabbixTuner',
    version='0.3',
    license='GNU LGPL 2.1',
    author='Janssen dos Reis Lima',
    author_email='janssenreislima@gmail.com',
    description='ZabbixTuner is a project that uses the Zabbix API that aims to verify a Zabbix installation and propose adjustments to improve system performance and stability.',
    py_modules=['ZabbixTuner'],
    packages=['conf'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    keywords='zabbix api tuner tuning',
    install_requires=['zabbix-api', 'termcolor', 'progressbar'],
    classifiers=[
         'Programming Language :: Python :: 2',
         'Development Status :: 5 - Production/Stable',
        ],
)
