# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal, InvalidOperation

from django import VERSION as DJANGO_VERSION
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test.utils import override_settings
from django.test import TestCase
from django.db import models

from .backends.base import BaseMapBackend
from .backends.yandex import YandexMapBackend
from .backends.google import GoogleMapBackend
from .fields import LatLongField, LatLong
from .forms import LatLongField as FormLatLongField
from .utils import get_backend, import_class
from .widgets import MapWidget, AdminMapWidget


class MyModel(models.Model):
    empty_point = LatLongField()
    null_point = LatLongField(blank=True, null=True)
    default_point = LatLongField(default=LatLong(33, 44))


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

    def test_latlog_field_change_invalid_value(self):
        self.assertRaises(ValidationError, MyModel.objects.create, empty_point='22.12345633.654321')

    def test_get_prep_value_convert(self):
        field = LatLongField()

        self.assertEqual(field.get_prep_value(''), '')
        self.assertEqual(field.get_prep_value(LatLong(22.123456, 33.654321)), LatLong(22.123456, 33.654321))
        self.assertIsNone(field.get_prep_value(None))

    def test_get_formfield(self):
        field = LatLongField()
        form_field = field.formfield()

        self.assertIsInstance(form_field, FormLatLongField)

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

    def test_load_without_backend(self):
        backend = get_backend({})
        self.assertEqual(backend.__class__.__name__, 'GoogleMapBackend')

    def test_load_not_subclass_mapbackend(self):
        self.assertRaises(ImproperlyConfigured, get_backend, {'BACKEND': 'django.test.TestCase'})


class ImportClassTestCase(TestCase):
    def test_import_from_string(self):
        c = import_class('django.test.TestCase')
        self.assertEqual(c, TestCase)

    def test_import_from_string_none(self):
        with self.assertRaises(ImportError):
            import_class('django.test.NonModel')


class BaseMapBackendTestCase(TestCase):
    def test_base_init(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.NAME, None)
        self.assertEqual(backend.API_URL, None)

    def test_base_get_js(self):
        backend = BaseMapBackend()

        self.assertRaises(ImproperlyConfigured, backend.get_js)

    def test_base_get_js_with_name(self):
        backend = BaseMapBackend()
        backend.NAME = 'test'

        self.assertEqual(
            backend.get_js(),
            'treasuremap/default/js/jquery.treasuremap-test.js'
        )

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

    @override_settings(TREASURE_MAP={'ADMIN_SIZE': (500, 500)})
    def test_base_admin_size_settings(self):
        backend = BaseMapBackend()

        self.assertEqual(backend.admin_width, 500)
        self.assertEqual(backend.admin_height, 500)

    @override_settings(TREASURE_MAP={'ADMIN_SIZE': ('Invalid',)})
    def test_base_admin_size_invalid_settings(self):
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


class GoogleMapBackendTestCase(TestCase):
    def test_get_api_js_default(self):
        backend = GoogleMapBackend()

        self.assertEqual(
            backend.get_api_js(),
            '//maps.googleapis.com/maps/api/js?v=3.exp'
        )

    @override_settings(TREASURE_MAP={'API_KEY': 'random_string'})
    def test_get_api_js_with_api_key(self):
        backend = GoogleMapBackend()

        self.assertEqual(
            backend.get_api_js(),
            '//maps.googleapis.com/maps/api/js?v=3.exp&key=random_string'
        )


class YandexMapBackendTestCase(TestCase):
    def test_get_api_js(self):
        backend = YandexMapBackend()

        self.assertEqual(
            backend.get_api_js(),
            '//api-maps.yandex.ru/2.1/?lang=en-us'
        )

    @override_settings(TREASURE_MAP={'API_KEY': 'random_string'})
    def test_get_api_js_with_api_key(self):
        backend = YandexMapBackend()

        self.assertEqual(
            backend.get_api_js(),
            '//api-maps.yandex.ru/2.1/?lang=en-us&pikey=random_string'
        )


class FormTestCase(TestCase):
    def test_witget_render(self):
        witget = MapWidget()
        done_html = '''
        {"latitude": 51.562519, "longitude": -1.603156, "zoom": 5}
        '''

        out_html = witget.render('name', LatLong(22.123456, 33.654321))
        self.assertTrue(out_html, done_html)

    def test_witget_render_js(self):
        witget = MapWidget()
        done_html = '''
        <script type="text/javascript" src="//maps.googleapis.com/maps/api/js?v=3.exp"></script>
        <script type="text/javascript" src="treasuremap/default/js/jquery.treasuremap-google.js"></script>
        '''

        out_html = str(witget.media)
        self.assertHTMLEqual(out_html, done_html)

    def test_admin_witget_render(self):
        witget = AdminMapWidget()
        done_html = '''
        {"latitude": 51.562519, "longitude": -1.603156, "zoom": 5}
        '''

        out_html = witget.render('name', LatLong(22.123456, 33.654321))
        self.assertTrue(out_html, done_html)

    def test_admin_witget_render_js(self):
        witget = AdminMapWidget()
        done_html = '''
        <script type="text/javascript" src="//maps.googleapis.com/maps/api/js?v=3.exp"></script>
        <script type="text/javascript" src="treasuremap/default/js/jquery.treasuremap-google.js"></script>
        '''

        out_html = str(witget.media)
        self.assertHTMLEqual(out_html, done_html)
