# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import smart_text
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

from .forms import LatLongField as FormLatLongField


class LatLong(object):
    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)

    def __repr__(self):
        return '<{}: {:.6f};{:.6f}>'.format(self.__class__.__name__, self.latitude, self.longitude)

    def __str__(self):
        return '{:.6f};{:.6f}'.format(self.latitude, self.longitude)


class LatLongField(with_metaclass(models.SubfieldBase, models.Field)):
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
        if not value:
            return None
        elif isinstance(value, LatLong):
            return value
        elif isinstance(value, (list, tuple)):
            return LatLong(latitude=value[0], longitude=value[1])
        else:
            args = value.split(';')

            if len(args) != 2:
                raise ValidationError(
                    self.error_messages['invalid_separator'], code='invalid', params={'value': value},
                )

            try:
                return LatLong(*args)
            except InvalidOperation:
                raise ValidationError(
                    self.error_messages['invalid'], code='invalid', params={'value': value},
                )

    def get_prep_value(self, value):
        if value:
            return str(value)
        elif value is None:
            return None
        return str(LatLong())

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': FormLatLongField,
        }
        defaults.update(kwargs)
        return super(LatLongField, self).formfield(**defaults)