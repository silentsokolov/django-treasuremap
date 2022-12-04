# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from treasuremap import fields


class MyModel(models.Model):
    empty_point = fields.LatLongField()
    null_point = fields.LatLongField(blank=True, null=True)
    default_point = fields.LatLongField(default=fields.LatLong(33, 44))
