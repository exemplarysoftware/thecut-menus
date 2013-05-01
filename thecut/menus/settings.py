# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


SELECTABLE_MODELS = getattr(settings, 'MENUS_SELECTABLE_MODELS',
                            ['menus.ViewLink', 'menus.WebLink'])
