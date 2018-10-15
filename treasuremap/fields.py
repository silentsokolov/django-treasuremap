# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal

from django import VERSION as DJANGO_VERSION
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

from .forms import LatLongField as FormLatLongField

if DJANGO_VERSION < (1, 8):
    DjangoModelFieldBase = with_metaclass(models.SubfieldBase, models.Field)
else:
    DjangoModelFieldBase = models.Field


class LatLong(object):
    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)

    @staticmethod
    def _equals_to_the_cent(a, b):
        return round(a, 6) == round(b, 6)

    @staticmethod
    def _no_equals_to_the_cent(a, b):
        return round(a, 6) != round(b, 6)

    @property
    def format_latitude(self):
        return '{:.6f}'.format(self.latitude)

    @property
    def format_longitude(self):
        return '{:.6f}'.format(self.longitude)

    def __repr__(self):
        return '<{}: {:.6f};{:.6f}>'.format(self.__class__.__name__, self.latitude, self.longitude)

    def __str__(self):
        return '{:.6f};{:.6f}'.format(self.latitude, self.longitude)

    def __eq__(self, other):
        return isinstance(other, LatLong) and (self._equals_to_the_cent(self.latitude, other.latitude) and
                                               self._equals_to_the_cent(self.longitude, other.longitude))

    def __ne__(self, other):
        return isinstance(other, LatLong) and (self._no_equals_to_the_cent(self.latitude, other.latitude) or
                                               self._no_equals_to_the_cent(self.longitude, other.longitude))


class LatLongField(DjangoModelFieldBase):
    description = _('Geographic coordinate system fields')
    default_error_messages = {
        'invalid': _("'%(value)s' both values must be a decimal number or integer."),
        'invalid_separator': _("As the separator value '%(value)s' must be ';'"),
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 24
        super(LatLongField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if value is None:
            return None
        elif not value:
            return LatLong()
        elif isinstance(value, LatLong):
            return value
        else:
            args = value.split(';')

            if len(args) != 2:
                raise ValidationError(
                    self.error_messages['invalid_separator'], code='invalid', params={'value': value},
                )

            return LatLong(*args)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super(LatLongField, self).get_prep_value(value)
        if value is None:
            return None

        value = self.to_python(value)

        return str(value)

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': FormLatLongField,
        }
        defaults.update(kwargs)
        return super(LatLongField, self).formfield(**defaults)
