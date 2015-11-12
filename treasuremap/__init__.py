# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


__author__ = 'Dmitriy Sokolov'
__version__ = '0.2.1'


default_app_config = 'treasuremap.apps.TreasureMapConfig'

if not hasattr(settings, 'TREASURE_MAP'):
    raise ImproperlyConfigured('The TREASURE_MAP setting is required.')
