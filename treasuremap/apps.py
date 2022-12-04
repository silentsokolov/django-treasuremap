# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TreasureMapConfig(AppConfig):
    name = "treasuremap"
    verbose_name = _("Treasure Map")
