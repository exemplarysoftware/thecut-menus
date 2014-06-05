# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from thecut.authorship.admin import AuthorshipMixin
from thecut.menus.models import ViewLink, WebLink

try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns


class ViewLinkAdmin(AuthorshipMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('name', 'view')}),
        ('Publishing', {'fields': (('publish_at', 'is_enabled'),),
                        'classes': ('collapse',)}),
    )
    list_display = ('name', 'view')

admin.site.register(ViewLink, ViewLinkAdmin)


class WebLinkAdmin(AuthorshipMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('name', 'url')}),
        ('Publishing', {'fields': (('publish_at', 'is_enabled'),),
                        'classes': ('collapse',)}),
    )
    list_display = ('name', 'url')

admin.site.register(WebLink, WebLinkAdmin)
