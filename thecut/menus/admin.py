# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import MenuItemAdminForm
from .models import MenuItem, ViewLink, WebLink
from django.conf.urls import include, url
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from thecut.authorship.admin import AuthorshipMixin


@admin.register(MenuItem)
class MenuItemAdmin(AuthorshipMixin, MPTTModelAdmin):

    fieldsets = [
        (None, {'fields': ['title', 'image', ('content_type', 'object_id'),
                           'parent', 'order']}),
        ('Publishing', {'fields': ['site', 'slug',
                                   ('publish_at', 'is_enabled'), 'expire_at',
                                   'publish_by', 'is_featured',
                                   ('created_at', 'created_by'),
                                   ('updated_at', 'updated_by')],
                        'classes': ['collapse']}),
    ]

    form = MenuItemAdminForm

    prepopulated_fields = {'slug': ['title']}

    readonly_fields = ['created_at', 'created_by', 'updated_at', 'updated_by']

    def get_urls(self):
        urlpatterns = [
            url(r'^api/', include('thecut.menus.api.urls')),
        ]
        urlpatterns += super(MenuItemAdmin, self).get_urls()
        return urlpatterns


@admin.register(ViewLink)
class ViewLinkAdmin(AuthorshipMixin, admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'view']}),
        ('Publishing', {'fields': [('publish_at', 'is_enabled')],
                        'classes': ['collapse']}),
    ]

    list_display = ['name', 'view']


@admin.register(WebLink)
class WebLinkAdmin(AuthorshipMixin, admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'url']}),
        ('Publishing', {'fields': [('publish_at', 'is_enabled')],
                        'classes': ['collapse']}),
    ]

    list_display = ['name', 'url']
