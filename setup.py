#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'gdriveshell',
    packages = ['gdriveshell'],
    version = '0.0.0',
    description = 'An FTP-style client for Google Drive',
    author = 'Marius Hårstad Bauer-Kjerkreit',
    author_email = 'mkjerkreit@gmail.com',
    url = 'https://github.com/thingol/gdriveshell',
    download_url = 'https://github.com/thingol/gdriveshell/tarball/0.0.0',
    license = 'BSD 2-Clause',
    keywords = ['google', 'drive', 'ftp', 'shell'],
    install_requires = [
        'httplib2',
        'google-api-python-client',
        'oauth2client'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD 2-Clause",
        "Programming Language :: Python :: 3"
    ]
)