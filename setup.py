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
    name='zabbix-tuner',
    url='https://github.com/gescheit/scripts',
    version='0.1',
    license='GNU LGPL 2.1',
    author='Janssen dos Reis Lima',
    author_email='janssenreislima@gmail.com',
    description='Zabbix Tuner',
    long_description=read('README.md'),
    py_modules=['zabbix_tuner'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
         'Programming Language :: Python',
         'Programming Language :: Python :: 2',
         'Development Status :: 2 - Pre-Alpha',
        ]
)
