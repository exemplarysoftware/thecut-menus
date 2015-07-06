# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


MENUITEM_IMAGES = getattr(settings, 'MENUS_MENUITEM_IMAGES', False)

SELECTABLE_MODELS = getattr(settings, 'MENUS_SELECTABLE_MODELS',
                            ['menus.ViewLink', 'menus.WebLink'])

SITE_FILTER = getattr(settings, 'MENUS_SITE_FILTER', False)
