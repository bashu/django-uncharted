django-uncharted
================

This is a `Django <http://djangoproject.com>`_ integration of `amCharts <http://amcharts.com>`_

Authored by `Basil Shubin <http://github.com/bashu>`_, inspired by `django-chartit <https://github.com/pgollakota/django-chartit>`_

.. image:: https://img.shields.io/pypi/v/django-uncharted.svg
    :target: https://pypi.python.org/pypi/django-uncharted/

.. image:: https://img.shields.io/pypi/dm/django-uncharted.svg
    :target: https://pypi.python.org/pypi/django-uncharted/

.. image:: https://img.shields.io/github/license/bashu/django-uncharted.svg
    :target: https://pypi.python.org/pypi/django-uncharted/

Installation
------------

Either clone this repository into your project, or install with ``pip install django-uncharted``

You'll need to add ``uncharted`` to ``INSTALLED_APPS`` in your project's ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS += [ 
        'uncharted',
    ]

Please see ``example`` application. This application is used to
manually test the functionalities of this package. This also serves as
a good example.

You need Django 1.4 or above to run that. It might run on older
versions but that is not tested.

External dependencies
~~~~~~~~~~~~~~~~~~~~~

* `amCharts <https://github.com/amcharts/amcharts2>`_ - This is not
  included in the package since it is expected that in most scenarios
  this would already be available.

Configuration (optional)
------------------------

Usage
-----

Templates
---------

Contributing
------------

If you've found a bug, implemented a feature or customized the
template and think it is useful then please consider contributing.
Patches, pull requests or just suggestions are welcome!

License
-------

``django-uncharted`` is released under the MIT license.
