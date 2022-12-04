# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .forms import LatLongField as FormLatLongField


@deconstructible
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
        return "{:.6f}".format(self.latitude)

    @property
    def format_longitude(self):
        return "{:.6f}".format(self.longitude)

    def __repr__(self):
        return "{}({:.6f}, {:.6f})".format(self.__class__.__name__, self.latitude, self.longitude)

    def __str__(self):
        return "{:.6f};{:.6f}".format(self.latitude, self.longitude)

    def __eq__(self, other):
        return isinstance(other, LatLong) and (
            self._equals_to_the_cent(self.latitude, other.latitude)
            and self._equals_to_the_cent(self.longitude, other.longitude)
        )

    def __ne__(self, other):
        return isinstance(other, LatLong) and (
            self._no_equals_to_the_cent(self.latitude, other.latitude)
            or self._no_equals_to_the_cent(self.longitude, other.longitude)
        )


class LatLongField(models.Field):
    description = _("Geographic coordinate system fields")
    default_error_messages = {
        "invalid": _("'%(value)s' both values must be a decimal number or integer."),
        "invalid_separator": _("As the separator value '%(value)s' must be ';'"),
    }

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 24
        super(LatLongField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if value is None:
            return None
        elif not value:
            return LatLong()
        elif isinstance(value, LatLong):
            return value
        else:
            if isinstance(value, (list, tuple, set)):
                args = value
            else:
                args = value.split(";")

            if len(args) != 2:
                raise ValidationError(
                    self.error_messages["invalid_separator"],
                    code="invalid",
                    params={"value": value},
                )

            return LatLong(*args)

    def get_db_prep_value(
        self, value, connection, prepared=False  # pylint: disable=unused-argument
    ):
        value = super(LatLongField, self).get_prep_value(value)
        if value is None:
            return None

        value = self.to_python(value)

        return str(value)

    def from_db_value(
        self, value, expression, connection, **kwargs
    ):  # pylint: disable=unused-argument
        return self.to_python(value)

    def formfield(self, _form_class=None, choices_form_class=None, **kwargs):
        return super(LatLongField, self).formfield(
            form_class=FormLatLongField, choices_form_class=choices_form_class, **kwargs
        )
