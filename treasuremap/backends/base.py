# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class BaseMapBackend(object):
    """
    Base map backend
    """
    NAME = None
    API_URL = None

    def __init__(self):
        self.options = getattr(settings, 'TREASURE_MAP', {})
        self.API_KEY = self.options.get('API_KEY', None)

        try:
            self.width = int(self.options.get('SIZE', (400, 400))[0])
            self.height = int(self.options.get('SIZE', (400, 400))[1])
        except (IndexError, ValueError):
            raise ImproperlyConfigured('Invalid SIZE parameter, use: (width, height).')

        try:
            self.admin_width = int(self.options.get('ADMIN_SIZE', (400, 400))[0])
            self.admin_height = int(self.options.get('ADMIN_SIZE', (400, 400))[1])
        except (IndexError, ValueError):
            raise ImproperlyConfigured('Invalid ADMIN SIZE parameter, use: (width, height).')

    def get_js(self):
        """
        Get jQuery plugin
        """
        if self.NAME is None:
            raise ImproperlyConfigured('Your use abstract class.')
        return 'treasuremap/default/js/jquery.treasuremap-{}.js'.format(self.NAME)

    def get_api_js(self):
        """
        Get javascript libraries
        """
        raise NotImplementedError()

    def get_widget_template(self):
        return self.options.get('WIDGET_TEMPLATE', 'treasuremap/widgets/map.html')

    @property
    def only_map(self):
        return self.options.get('ONLY_MAP', True)

    def get_map_options(self):
        map_options = self.options.get('MAP_OPTIONS', {})
        map_options = OrderedDict(
            sorted(map_options.items(), key=lambda x: x[1], reverse=True)
        )

        if not map_options.get('latitude'):
            map_options['latitude'] = 51.562519

        if not map_options.get('longitude'):
            map_options['longitude'] = -1.603156

        if not map_options.get('zoom'):
            map_options['zoom'] = 5

        return map_options
