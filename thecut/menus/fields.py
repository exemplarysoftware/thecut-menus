# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes.fields import GenericForeignKey


class MenuItemGenericForeignKey(GenericForeignKey):

    def _check_content_type_field(self):
        # TODO Custom check for MenuItemContentType?
        return []
