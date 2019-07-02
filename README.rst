################################################################################
transmart-hyper-dicer slicing tool for tranSMART
################################################################################

|Build status| |codecov| |pypi| |downloads|

.. |Build status| image:: https://travis-ci.org/thehyve/transmart-hyper-dicer.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/thehyve/transmart-hyper-dicer/branches
.. |codecov| image:: https://codecov.io/gh/thehyve/transmart-hyper-dicer/branch/master/graph/badge.svg
   :alt: codecov
   :target: https://codecov.io/gh/thehyve/transmart-hyper-dicer
.. |pypi| image:: https://img.shields.io/pypi/v/transmart-hyper-dicer.svg
   :alt: PyPI
   :target: https://pypi.org/project/transmart-hyper-dicer/
.. |downloads| image:: https://img.shields.io/pypi/dm/transmart-hyper-dicer.svg
   :alt: PyPI - Downloads
   :target: https://pypi.org/project/transmart-hyper-dicer/

transmart-hyper-dicer is a data slicing tool that reads data from one TranSMART_ instance and uploads it to another. 

⚠️ Note: this is a very preliminary version, still under development.
Issues can be reported at https://github.com/thehyve/transmart-hyper-dicer/issues.

.. _TranSMART: https://github.com/thehyve/transmart_core

Configuration
-------------

Connection to Keycloak identity provider and tranSMART is configured by setting the environment variables below:

+---------------------+--------------------------------------------------------------------------------------+
| Variable            | Description                                                                          |
+=====================+======================================================================================+
| TRANSMART_URL       | URL of the TranSMART back-end application e.g. `https://transmart.example.com`       |
+---------------------+--------------------------------------------------------------------------------------+
| KEYCLOAK_SERVER_URL | URL of the Keycloak identity provider e.g. `https://keycloak.example.com`            |
+---------------------+--------------------------------------------------------------------------------------+
| KEYCLOAK_REALM      | Keycloak realm, e.g. `dev`                                                           |
+---------------------+--------------------------------------------------------------------------------------+
| KEYCLOAK_CLIENT_ID  | Keycloak client ID, e.g. `transmart-client`                                          |
+---------------------+--------------------------------------------------------------------------------------+
| OFFLINE_TOKEN       | An offline token used used as a refresh token in order to communicate with TranSMART |
+---------------------+--------------------------------------------------------------------------------------+

In order to generate an offline token for `USERNAME` user, the following `curl` command can be used.
To get the token the user needs to have the role mapping for the realm-level: `"offline_access"`.
Before using the command you have to substitute words in uppercase with proper ones.

.. code-block:: bash

    curl \
      -d 'client_id=KEYCLOAK_CLIENT_ID' \
      -d 'username=USERNAME' \
      -d 'password=PASSWORD' \
      -d 'grant_type=password' \
      -d 'scope=offline_access' \
      'https://KEYCLOAK_SERVER_URL/auth/realms/KEYCLOAK_REALM/protocol/openid-connect/token'


The value of the `refresh_token` field in the response is the offline token.

Installation
------------

The package requires Python 3.6+.

To install ``transmart-hyper-dicer``, do:

.. code-block:: bash

  pip install transmart-hyper-dicer

Or from source:

.. code-block:: bash

  git clone https://github.com/thehyve/transmart-hyper-dicer.git
  cd transmart-hyper-dicer
  pip install .


Run tests (including coverage) with:

.. code-block:: bash

  python setup.py test


Usage
-----

In progress...


Package management and dependencies
-----------------------------------

This project uses `pip` for installing dependencies and package management.

* Dependencies should be added to `setup.py` in the `install_requires` list.


License
-------

Copyright (c) 2019 The Hyve B.V.

The Transmart Hyper Dicer is licensed under the MIT License. See the file `<LICENSE>`_.
