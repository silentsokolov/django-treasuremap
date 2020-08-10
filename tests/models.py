# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from treasuremap import fields
from django.db import models


class MyModel(models.Model):
    empty_point = fields.LatLongField()
    null_point = fields.LatLongField(blank=True, null=True)
    default_point = fields.LatLongField(default=fields.LatLong(33, 44))
