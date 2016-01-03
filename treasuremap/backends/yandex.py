# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from django.conf import settings

from .base import BaseMapBackend


class YandexMapBackend(BaseMapBackend):
    NAME = 'yandex'
    API_URL = '//api-maps.yandex.ru/2.1/'

    def get_api_js(self):
        params = OrderedDict()
        params['lang'] = settings.LANGUAGE_CODE

        if self.API_KEY:
            params['pikey'] = self.API_KEY

        return '{js_lib}?{params}'.format(js_lib=self.API_URL, params=urlencode(params))
