from django.test import TestCase

from .fields import LatLongField


class TestPositionField(TestCase):
    def test_deconstruct(self):
        field = LatLongField()
        name, path, args, kwargs = field.deconstruct()
        new_instance = LatLongField(*args, **kwargs)
        self.assertEqual(field.max_length, new_instance.max_length)