# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import urllib

from django.conf import settings

from .base import BaseMapBackend


class YandexMapBackend(BaseMapBackend):
    NAME = 'yandex'
    API_URL = '//api-maps.yandex.ru/2.1/'

    def get_api_js(self):
        params = {'lang': settings.LANGUAGE_CODE}

        if self.API_KEY:
            params['pikey'] = self.API_KEY

        return '{js_lib}?{params}'.format(js_lib=self.API_URL, params=urllib.urlencode(params))