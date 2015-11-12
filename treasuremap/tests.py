# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal, InvalidOperation

from django import VERSION as DJANGO_VERSION

from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test.utils import override_settings
from django.test import TestCase
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible

from .backends.base import BaseMapBackend
from .fields import LatLongField, LatLong
from .utils import get_backend


@python_2_unicode_compatible
class MyModel(models.Model):
    empty_point = LatLongField()
    null_point = LatLongField(blank=True, null=True)
    default_point = LatLongField(default=LatLong(33, 44))

    def __str__(self):
        return force_text(self.name)


class LatLongObjectTestCase(TestCase):
    def test_create_empty_latlong(self):
        latlong = LatLong()
        self.assertEqual(latlong.latitude, 0.0)
        self.assertEqual(latlong.longitude, 0.0)

    def test_create_latlog_with_float(self):
        latlong = LatLong(latitude=33.300, longitude=44.440)
        self.assertEqual(latlong.latitude, Decimal(33.300))
        self.assertEqual(latlong.longitude, Decimal(44.440))

    def test_create_latlog_with_string(self):
        latlong = LatLong(latitude='33.300', longitude='44.440')
        self.assertEqual(latlong.latitude, Decimal('33.300'))
        self.assertEqual(latlong.longitude, Decimal('44.440'))

    def test_create_latlog_with_invalid_value(self):
        self.assertRaises(InvalidOperation, LatLong, 'not int', 44.440)

    def test_latlog_object_str(self):
        latlong = LatLong(latitude=33.300, longitude=44.440)
        self.assertEqual(str(latlong), '33.300000;44.440000')

    def test_latlog_object_repr(self):
        latlong = LatLong(latitude=33.300, longitude=44.440)
        self.assertEqual(repr(latlong), '<LatLong: 33.300000;44.440000>')

    def test_latlog_object_eq(self):
        self.assertEqual(LatLong(latitude=33.300, longitude=44.440), LatLong(latitude=33.300, longitude=44.440))

    def test_latlog_object_ne(self):
        self.assertNotEqual(LatLong(latitude=33.300, longitude=44.441), LatLong(latitude=22.300, longitude=44.441))


class LatLongFieldTestCase(TestCase):
    def test_latlog_field_create(self):
        m = MyModel.objects.create()
        new_m = MyModel.objects.get(pk=m.pk)

        self.assertEqual(new_m.empty_point, LatLong())
        self.assertEqual(new_m.null_point, None)
        self.assertEqual(new_m.default_point, LatLong(33, 44))

    def test_latlog_field_change_with_latlog_obj(self):
        m = MyModel.objects.create(empty_point=LatLong(22.123456, 33.654321))
        new_m = MyModel.objects.get(pk=m.pk)

        self.assertEqual(new_m.empty_point, LatLong(22.123456, 33.654321))

    def test_latlog_field_change_with_string(self):
        m = MyModel.objects.create(empty_point='22.123456;33.654321')
        new_m = MyModel.objects.get(pk=m.pk)

        self.assertEqual(new_m.empty_point, LatLong(22.123456, 33.654321))

    def test_latlog_field_change_with_list(self):
        m = MyModel.objects.create(empty_point=[22.123456, 33.654321])
        new_m = MyModel.objects.get(pk=m.pk)

        self.assertEqual(new_m.empty_point, LatLong(22.123456, 33.654321))

    def test_latlog_field_change_invalid_value(self):
        self.assertRaises(ValidationError, MyModel.objects.create, empty_point='22.12345633.654321')

    def test_deconstruct(self):
        if DJANGO_VERSION >= (1, 7):
            field = LatLongField()
            name, path, args, kwargs = field.deconstruct()
            new_instance = LatLongField(*args, **kwargs)
            self.assertEqual(field.max_length, new_instance.max_length)


class LoadBackendTestCase(TestCase):
    def test_load_google(self):
        backend = get_backend({'BACKEND': 'treasuremap.backends.google.GoogleMapBackend'})
        self.assertEqual(backend.__class__.__name__, 'GoogleMapBackend')

    def test_load_yandex(self):
        backend = get_backend({'BACKEND': 'treasuremap.backends.yandex.YandexMapBackend'})
        self.assertEqual(backend.__class__.__name__, 'YandexMapBackend')

    def test_load_failed(self):
        self.assertRaises(ImportError, get_backend, {'BACKEND': 'treasuremap.backends.unknown.UnknownMapBackend'})


class BaseMapBackendTestCase(TestCase):
    def test_base_init(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.NAME, None)
        self.assertEqual(backend.API_URL, None)

    def test_base_get_js(self):
        backend = BaseMapBackend()

        self.assertRaises(ImproperlyConfigured, backend.get_js)

    def test_base_get_api_js(self):
        backend = BaseMapBackend()

        self.assertRaises(NotImplementedError, backend.get_api_js)

    def test_base_widget_template_default(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.get_widget_template(), 'treasuremap/widgets/map.html')

    @override_settings(TREASURE_MAP={'WIDGET_TEMPLATE': 'template/custom.html'})
    def test_base_widget_template_custom(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.get_widget_template(), 'template/custom.html')

    def test_base_api_key_default(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.API_KEY, None)

    @override_settings(TREASURE_MAP={'API_KEY': 'random_string'})
    def test_base_api_key_settings(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.API_KEY, 'random_string')

    def test_base_only_map_default(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.only_map, True)

    @override_settings(TREASURE_MAP={'ONLY_MAP': False})
    def test_base_only_map_settings(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.only_map, False)

    def test_base_size_default(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.width, 400)
        self.assertEqual(backend.height, 400)

    @override_settings(TREASURE_MAP={'SIZE': (500, 500)})
    def test_base_size_settings(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.width, 500)
        self.assertEqual(backend.height, 500)

    @override_settings(TREASURE_MAP={'SIZE': ('Invalid',)})
    def test_base_size_invalid_settings(self):
        self.assertRaises(ImproperlyConfigured, BaseMapBackend)

    def test_base_map_options_default(self):
        backend = BaseMapBackend()

        self.assertDictEqual(
            backend.get_map_options(),
            {'latitude': 51.562519, 'longitude': -1.603156, 'zoom': 5}
        )

    @override_settings(TREASURE_MAP={'MAP_OPTIONS': {'latitude': 44.1, 'longitude': -55.1, 'zoom': 1}})
    def test_base_map_options_settings(self):
        backend = BaseMapBackend()

        self.assertDictEqual(
            backend.get_map_options(),
            {'latitude': 44.1, 'longitude': -55.1, 'zoom': 1}
        )
