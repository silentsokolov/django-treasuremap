django-treasuremap
==================

django-treasuremap app, makes it easy to store and display the location on the map using different providers (Google, Yandex).


Requirements
------------

* Python 2.7+ or Python 3.3+
* Django 1.7+


Installation
------------

Use your favorite Python package manager to install the app from PyPI, e.g.

Example:

``pip install django-treasuremap``


Add ``treasuremap`` to ``INSTALLED_APPS``:

Example:

.. code:: python

    INSTALLED_APPS = (
        ...
        'treasuremap',
        ...
    )

Configuration
-------------

Within your settings.py, you’ll need to add a setting (which backend to use, etc).

Example:

.. code:: python

    TREASURE_MAP = {
        'BACKEND': 'treasuremap.backends.google.GoogleMapBackend',
        'API_KEY': 'Your API key',
        'SIZE': (400, 600),
        'MAP_OPTIONS': {
            'zoom': 5
        }
    }


Example usage
-------------

In models
~~~~~~~~~

.. code:: python

    from django.db import models
    from treasuremap.fields import LatLongField

    class ShopModel(models.Model):
        name = models.CharField(max_length=100)
        point = LatLongField(blank=True)


In forms
~~~~~~~~

.. code:: python

    from django import forms
    from treasuremap.forms import LatLongField

    class ShopForm(models.Model):
        point = LatLongField()


.. code:: html

    <form method="POST" action=".">
        {{ form.media }}
        {% csrf_token %}
        {{ form.as_p }}
    </form>


Depending on what backend you are using, the correct widget will be displayed
with a marker at the currently position (jQuery is required).

.. image:: docs/screenshot.png


Settings
--------

Support map:
~~~~~~~~~~~~

- Google map ``treasuremap.backends.google.GoogleMapBackend``
- Yandex map ``treasuremap.backends.yandex.YandexMapBackend``


Other settings:
~~~~~~~~~~~~~~~

- ``API_KEY`` - if need, default ``None``
- ``SIZE`` - tuple with the size of the map, default ``(400, 400)``
- ``MAP_OPTIONS`` - dict, used to initialize the map, default ``{'latitude': 51.562519, 'longitude': -1.603156, 'zoom': 5}``. ``latitude`` and ``longitude`` is required, do not use other "LatLong Object".