==========
pyswitcheo
==========


.. image:: https://github.com/ansrivas/pyswitcheo/blob/master/docs/source/_static/2.png
   :width: 100px
   :height: 100px
   :alt: Switcheo Decentralized Exchange
   :align: left

|License: MIT| |CircleCI| |Coverage| |Documentation|

**pyswitcheo** is a simple python client to interact with `Switcheo Decentralized Exchange <https://switcheo.exchange/>`_

Current Stable Version
----------------------

::

    0.1.0

Installation
------------

pip
~~~

.. code-block:: bash

  $ pip install pyswitcheo


Getting Started
----------------

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


Development Installation
-------------------------


-  This project uses ``pipenv`` for python environment management.
-  Download/Install ``pipenv`` like this ``pip install --user pipenv``
-  Clone the project.
-  Inside the project directory run ``pipenv install``.
-  This will create a python virtualenv which can be activated using ``pipenv shell``.
-  Now install the application in editable mode and you are ready to
   start development

   ::

       $ pip install -e .

Test
----

To run the tests:

::

    make test


-------

Documentation theme is highly inspired by `Aiohttp <http://docs.aiohttp.org/en/stable/>`_.


.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |CircleCI| image:: https://circleci.com/gh/ansrivas/pyswitcheo.svg?style=svg
   :target: https://circleci.com/gh/ansrivas/pyswitcheo
.. |Coverage| image:: https://coveralls.io/repos/github/ansrivas/pyswitcheo/badge.svg
   :target: https://coveralls.io/github/ansrivas/pyswitcheo
.. |Documentation| image:: https://readthedocs.org/projects/test-repo-2/badge/?version=latest
  :target: https://test-repo-2.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
