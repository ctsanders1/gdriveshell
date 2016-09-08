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
~/.gdriveshell/oauth2 file. When you first start gdriveshell the authentication process will
proceed.

    Go to the Google developer console
    Create a new project for gdriveshell
    Click on "Dashboard" on the sidebar
    Then "ENABLE API" on the Dashboard
    Enable the Drive API and click "Go to Credentials"
    Under "Where will you... " choose "Other UI (e.g. Windows, CLI tool)"
    and "User data" under "What data..."
    Pick a suitable name as your Client ID.
    The consent screen requires a "Product name" but is otherwise not important.
    Download your new credentials (file name: client_id.json)
    and put them in the folder ~/.gdriveshell/

# Python Version
Developed using 3.5.1

# Third Party Libraries and Dependencies

* [google-api-python-client-py3](https://pypi.python.org/pypi/google-api-python-client-py3/)
* [httplib2](https://pypi.python.org/pypi/httplib2/)
* [colorama](https://pypi.python.org/pypi/colorama/)

# Contributing
Any time. 2-clause BSD license.
