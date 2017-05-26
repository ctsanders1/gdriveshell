# About
Simple ftp-style client.

# Installation
To install, simply use `pip` or `easy_install`:

```bash
$ pip install --upgrade gdriveshell
```
or
```bash
$ easy_install --upgrade gdriveshell
```

# Authentication

OAuth2 is used for authenticating against Google. The resulting token is placed in the
~/.gdriveshell/credentials file. When you first start gdriveshell the authentication
process will proceed.

* Go to the Google developer console
* Create a new project for gdriveshell
* Click on "Library" on the sidebar
* Then choose on "Drive API" under "Google Apps APIs"
* Click on "Credentials" on the sidebar
* Click on the  "Create credentials" button and choose "OAuth ID"
* Choose "Other" as your "Application type"
* Pick a suitable name as for your credentials.
* The consent screen requires a "Product name" but is otherwise not important.
* Put your id and secret in the folder ~/.gdriveshell/config

```
    [auth]
      client_id = <your id>
      client_sec = <your secret>
```

# Python Version
Developed using 3.5.1

# Third Party Libraries and Dependencies

* [google-api-python-client-py3](https://pypi.python.org/pypi/google-api-python-client-py3/)
* [httplib2](https://pypi.python.org/pypi/httplib2/)
* [colorama](https://pypi.python.org/pypi/colorama/)

# Contributing
Any time. 2-clause BSD license.
