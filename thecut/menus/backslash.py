# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut import backslash
from thecut.menus.models import MenuItem


class MenuItemBackslash(backslash.ModelAdmin):

    class Meta(object):
        model = MenuItem

    def get_queryset(self, *args, **kwargs):
        queryset = super(MenuItemBackslash, self).get_queryset(*args, **kwargs)
        # Only display top-level menus for editing in backslash.
        return queryset.filter(object_id__isnull=True, parent__isnull=True)
