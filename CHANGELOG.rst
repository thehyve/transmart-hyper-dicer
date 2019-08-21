###########
Change Log
###########

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.

[Unreleased]
************


[0.1.2]
************

Changed
-------

* Fix mapping for observations without end time.
* Skip subtrees without study or concept nodes in ontology mapping.
* Fix for handling 'VERIFY_CERT' env variable.


[0.1.1]
************

Changed
-------

* Fix for handling 'VERIFY_CERT' env variable.


[0.1.0]
************

Added
-----

* Support for loading study metadata and tree node tags.
* Support for slicing without trial visit dimension in the hypercube.
* Support for configuring requests verify option.
* Reading .env file from the current working directory.

Changed
-------

* Updated dependencies: transmart-loader version to 1.2.0
* Project README.


[0.0.1]
************

Added
-----

* Initial TranSMART hyper dicer package
