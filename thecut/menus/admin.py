# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from thecut.authorship.admin import AuthorshipMixin
from thecut.menus.forms import MenuItemAdminForm
from thecut.menus.models import MenuItem, ViewLink, WebLink

try:
    from django.conf.urls import include, patterns
except ImportError:
    from django.conf.urls.defaults import include, patterns


class MenuItemAdmin(AuthorshipMixin, MPTTModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    form = MenuItemAdminForm

    def get_urls(self):
        urlpatterns = patterns(
            '',
            (r'^api/', include('thecut.menus.api.urls')),
        )
        urlpatterns += super(MenuItemAdmin, self).get_urls()
        return urlpatterns

admin.site.register(MenuItem, MenuItemAdmin)


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
