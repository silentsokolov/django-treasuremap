# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .base import BaseMapBackend


class GoogleMapBackend(BaseMapBackend):
    NAME = 'google'
    API_URL = '//maps.googleapis.com/maps/api/js'

    def get_api_js(self):
        params = OrderedDict()
        params['v'] = '3.exp'

        if self.API_KEY:
            params['key'] = self.API_KEY

        return '{js_lib}?{params}'.format(js_lib=self.API_URL, params=urlencode(params))
