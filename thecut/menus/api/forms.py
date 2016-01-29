# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from ..models import MenuItem


class MenuItemFilterForm(forms.Form):
    """
    A :py:class:`~django.forms.Form` for filtering
    :py:class:`~thecut.menus.models.MenuItem` instances.

    """

    root = forms.ModelChoiceField(queryset=MenuItem.objects.none(),
                                  required=False)

    def __init__(self, *args, **kwargs):
        super(MenuItemFilterForm, self).__init__(**kwargs)
        self.fields['root'].queryset = self.get_menuitem_queryset()

    def get_menuitem_queryset(self):
        return MenuItem.objects.all()

    def filter_queryset(self, queryset):
        self.is_valid()
        # Return only the children of the root MenuItem, if one has
        # been specified.
        root = self.cleaned_data.get('root')
        if root:
            return root.get_children()

        return MenuItem.objects.all()
