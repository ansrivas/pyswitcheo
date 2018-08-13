.. pyswitcheo documentation master file, created by
   sphinx-quickstart on Tue Aug  7 22:17:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


======================
Welcome to PySwitcheo
======================

.. image:: https://raw.githubusercontent.com/ansrivas/pyswitcheo/master/docs/source/_static/2.png
   :width: 100px
   :height: 100px
   :alt: Switcheo Decentralized Exchange
   :align: left

|License: MIT| |CircleCI| |Coverage| |Documentation|

**pyswitcheo** is a simple python client to interact with `Switcheo Decentralized Exchange <https://switcheo.exchange/>`_

.. _GitHub: https://github.com/ansrivas/pyswitcheo


Installation
====================

.. code-block:: bash

  $ pip install pyswitcheo

Getting Started
===============

Client example

.. code-block:: python

  import json
  from http import HTTPStatus
  from pyswitcheo.api import SwitcheoApi

  if __name__ == '__main__':
      client = SwitcheoApi(base_url="https://test-api.switcheo.network")

      resp = client.list_contracts()
      if resp.status_code == HTTPStatus.OK:
          print(json.loads(resp.text.encode("UTF-8")))


More examples are located at `examples <https://github.com/ansrivas/pyswitcheo/examples>`_

Source code
===========

The project is hosted on GitHub_

Please feel free to file an issue on the `bug tracker
<https://github.com/ansrivas/pyswitcheo/issues>`_ if you have found a bug
or have some suggestion in order to improve the library.

Dependencies
============

- Python 3.5.3+
- neo-core


Authors and License
===================

The ``pyswitcheo`` package is written by Ankur Srivastava.

It's MIT licensed and freely available.

Feel free to improve this package and send a pull request to GitHub_.


Documentation
=================

.. toctree::
   :name: mastertoc
   :maxdepth: 2

   documentation
   ratelimits
   endpoints

.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
  :target: https://opensource.org/licenses/MIT
.. |CircleCI| image:: https://circleci.com/gh/ansrivas/pyswitcheo.svg?style=svg
  :target: https://circleci.com/gh/ansrivas/pyswitcheo
.. |Coverage| image:: https://coveralls.io/repos/github/ansrivas/pyswitcheo/badge.svg
  :target: https://coveralls.io/github/ansrivas/pyswitcheo
.. |Documentation| image:: https://readthedocs.org/projects/pyswitcheo/badge/?version=latest
  :target: https://pyswitcheo.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
