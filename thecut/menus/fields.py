# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:  # pre Django 1.7 compatibility
    from django.contrib.contenttypes.generic import GenericForeignKey


class MenuItemGenericForeignKey(GenericForeignKey):

    def _check_content_type_field(self):
        # TODO Custom check for MenuItemContentType?
        return []
