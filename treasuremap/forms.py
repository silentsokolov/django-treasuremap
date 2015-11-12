# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .widgets import MapWidget


class LatLongField(forms.MultiValueField):
    widget = MapWidget
    default_error_messages = {
        'invalid_coordinates': _('Enter a valid coordinate.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        fields = (
            forms.DecimalField(label=_('latitude')),
            forms.DecimalField(label=_('longitude')),
        )

        super(LatLongField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                raise ValidationError(
                    self.error_messages['invalid_coordinates'], code='invalid'
                )
            if data_list[1] in self.empty_values:
                raise ValidationError(
                    self.error_messages['invalid_coordinates'], code='invalid'
                )
            return data_list
        return None
