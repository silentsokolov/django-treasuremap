# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import importlib

from django.core.exceptions import ImproperlyConfigured

from .backends.base import BaseMapBackend


def import_class(path):
    path_bits = path.split('.')
    class_name = path_bits.pop()
    module_path = '.'.join(path_bits)
    module_itself = importlib.import_module(module_path)

    if not hasattr(module_itself, class_name):
        raise ImportError('The Python module {} has no {} class.'.format(module_path, class_name))

    return getattr(module_itself, class_name)


def get_backend(map_config):
    if not map_config.get('BACKEND'):
        map_config['BACKEND'] = 'treasuremap.backends.google.GoogleMapBackend'

    backend = import_class(map_config['BACKEND'])

    if not issubclass(backend, BaseMapBackend):
        raise ImproperlyConfigured('Is backend {} is not instance BaseMapBackend.'.format(backend))

    return backend()
