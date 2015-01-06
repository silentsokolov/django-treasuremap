# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import urllib

from .base import BaseMapBackend


class GoogleMapBackend(BaseMapBackend):
    NAME = 'google'
    API_URL = '//maps.googleapis.com/maps/api/js'

    def get_api_js(self):
        params = {'v': '3.exp'}

        if self.API_KEY:
            params['key'] = self.API_KEY

        return '{js_lib}?{params}'.format(js_lib=self.API_URL, params=urllib.urlencode(params))