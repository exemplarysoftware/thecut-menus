# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import MenuItem
from django import forms
from mptt.forms import MPTTAdminForm


class MenuItemAdminForm(MPTTAdminForm):

    class Meta(object):
        model = MenuItem

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = True

    def clean_slug(self, *args, **kwargs):
        # Allow the `slug` field to be nullable, even though it's a
        # text field in the database.
        slug = self.cleaned_data.get('slug')

        if not slug:
            return None

        return slug


class MenuItemBackslashForm(forms.ModelForm):
    """Form for adding/editing a top-level root MenuItem."""

    class Meta(object):
        model = MenuItem

    def __init__(self, *args, **kwargs):
        super(MenuItemBackslashForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['slug'].required = True
