# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from thecut import backslash
from thecut.authorship.admin import AuthorshipMixin
from .models import MenuItem


class MenuBackslashForm(forms.ModelForm):

    class Meta(object):
        model = MenuItem

    def __init__(self, *args, **kwargs):
        super(MenuBackslashForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['slug'].required = True


class MenuBackslash(AuthorshipMixin, backslash.ModelAdmin):
    """Backslash class for adding a 'menu'.

    A 'menu' is just a `MenuItem` without a `parent` or
    `context_object`.

    """

    form = MenuBackslashForm
    fieldsets = [
        (None, {'fields': ['name', 'slug']}),
        ('Publishing', {'fields': [('publish_at', 'is_enabled'),
                                   ('expire_at')]}),
    ]

    class Meta(object):
        model = MenuItem

    def get_queryset(self, *args, **kwargs):
        queryset = super(MenuItemBackslash, self).get_queryset(*args, **kwargs)
        # Only display top-level menus for editing in backslash.
        return queryset.filter(object_id__isnull=True, parent__isnull=True)
