# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.conf import settings
from django import forms
from django.forms import MultiWidget
from django.template.loader import render_to_string

from .utils import get_backend


class MapWidget(MultiWidget):
    def __init__(self, attrs=None):
        self.map_backend = get_backend(settings.TREASURE_MAP)

        if self.map_backend.only_map:
            widgets = (
                forms.HiddenInput(), forms.HiddenInput(),
            )
        else:
            widgets = (
                forms.NumberInput(), forms.NumberInput(),
            )

        super(MapWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.format_latitude, value.format_longitude]
        return [None, None]

    @property
    def is_hidden(self):
        return False

    def get_context_widgets(self):
        context = {
            'map_options': json.dumps(self.map_backend.get_map_options()),
            'width': self.map_backend.width,
            'height': self.map_backend.height,
            'only_map': self.map_backend.only_map,
        }
        return context

    def format_output(self, rendered_widgets):
        context = self.get_context_widgets()

        context['latitude'] = rendered_widgets[0]
        context['longitude'] = rendered_widgets[1]

        return render_to_string(self.map_backend.get_widget_template(), context)

    def _get_media(self):
        media = forms.Media()
        for w in self.widgets:
            media = media + w.media

        media._js += (
            self.map_backend.get_api_js(),
            self.map_backend.get_js()
        )
        return media
    media = property(_get_media)


class AdminMapWidget(MapWidget):
    def get_context_widgets(self):
        context = super(AdminMapWidget, self).get_context_widgets()

        context['width'] = self.map_backend.admin_width
        context['height'] = self.map_backend.admin_height

        return context
