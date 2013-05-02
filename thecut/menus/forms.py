# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.contrib.contenttypes.models import ContentType
from thecut.menus import settings
from thecut.menus.models import Menu, MenuItem, ViewLink, WebLink
from thecut.menus.widgets import ImageInput


class MenuItemInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MenuItemInlineForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].label = 'Target'
        self.fields['object_id'].label = 'Object'

        content_types = []
        for app_model in settings.SELECTABLE_MODELS:
            app_label, model = app_model.lower().split('.')
            content_types += [ContentType.objects.get(
                app_label=app_label, model=model)]
        queryset = self.fields['content_type'].queryset
        self.fields['content_type'].queryset = queryset.filter(
            pk__in=[ct.pk for ct in content_types])

    class Media(object):
        css = {'all': ['menus/menuitem_inline.css']}
        js = ['javascripts/jquery.js', 'javascripts/jquery-ui.js',
              'menus/menuitem_inline.js']

    class Meta(object):
        model = MenuItem


class MenuItemAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        if not settings.MENUITEM_IMAGES:
            del self.fields['image']
        self.fields['content_type'].label = 'Type'
        self.fields['object_id'].label = 'Target'

        content_types = []
        for app_model in settings.SELECTABLE_MODELS:
            app_label, model = app_model.lower().split('.')
            content_types += [ContentType.objects.get(
                app_label=app_label, model=model)]
        queryset = self.fields['content_type'].queryset
        self.fields['content_type'].queryset = queryset.filter(
            pk__in=[ct.pk for ct in content_types])

    class Meta:
        fields = ('name', 'content_type', 'object_id', 'image', 'is_enabled')
        model = MenuItem
        widgets = {'image': ImageInput()}


class SubMenuItemAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubMenuItemAdminForm, self).__init__(*args, **kwargs)
        if not settings.MENUITEM_IMAGES:
            del self.fields['image']

    class Meta:
        fields = ('name', 'image', 'is_enabled')
        model = MenuItem
        widgets = {'image': ImageInput()}
