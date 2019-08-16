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
| VERIFY_CERT         | Either a boolean, in which case it controls whether the server’s                     |
|                     | TLS certificate is verified, or a string, in which case it must be a path            |
|                     | to a CA bundle to use. Defaults to True.                                             |
+---------------------+--------------------------------------------------------------------------------------+

In order to generate an offline token for ``USERNAME`` user, the following ``curl`` command can be used.
To get the token the user needs to have the role mapping for the realm-level: ``offline_access``.
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

All the variables can be specified in the ``.env`` file as key-value pairs. They will be automatically set as environment variables, when starting the application. Example of the ``.env`` file:

.. code-block:: bash

   KEYCLOAK_CLIENT_ID=transmart-client
   KEYCLOAK_SERVER_URL=https://keycloak.example.com
   KEYCLOAK_REALM=dev
   OFFLINE_TOKEN=<refresh_token value from the curl response>
   TRANSMART_URL=https://transmart.example.com


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

Read subset of data from the configured tranSMART instance, based on the constraint specified in an input JSON file
and write the output in transmart-copy_ format to /path/to/output.
The output directory should be empty of not existing (then it will be created).

Input constraint has to be a `valid tranSMART constraint`_. Example of <input.json> file content:

.. code-block:: JSON

  {
    "type": "study_name",
    "studyId": "EHR"
  }


Run:

.. code-block:: bash

  transmart-hyper-dicer <input.json> /path/to/output


This generates the directories ``i2b2metadata`` and ``i2b2demodata`` in the ``output`` directory.
The generated data can be loaded using transmart-copy_:

.. code-block:: console

  # Download transmart-copy:
  curl -f -L https://repo.thehyve.nl/service/local/repositories/releases/content/org/transmartproject/transmart-copy/17.1-HYVE-6.2/transmart-copy-17.1-HYVE-6.2.jar -o transmart-copy.jar
  # Load data
  PGUSER=tm_cz PGPASSWORD=tm_cz java -jar transmart-copy.jar -d output


.. _transmart-copy: https://github.com/thehyve/transmart-core/tree/dev/transmart-copy
.. _`valid tranSMART constraint`: https://transmart.thehyve.net/open-api/index.html

Package management and dependencies
-----------------------------------

This project uses `pip` for installing dependencies and package management.

* Dependencies should be added to `setup.py` in the `install_requires` list.


License
-------

Copyright (c) 2019 The Hyve B.V.

The Transmart Hyper Dicer is licensed under the MIT License. See the file `<LICENSE>`_.
