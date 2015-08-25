# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from django.db.models import Q
from thecut import backslash
from .admin import MenuItemAdmin
from .forms import MenuItemBackslashForm
from .models import MenuItem

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    # Django < 1.7 compatibility.
    from django.contrib.sites.models import get_current_site


class MenuItemBackslash(MenuItemAdmin, backslash.ModelAdmin):
    """Add and a top-level root MenuItem and manage it's children."""

    form = MenuItemBackslashForm

    fieldsets = [
        (None, {'fields': ['title', 'slug']}),
        ('Publishing', {'fields': ['site', ('publish_at', 'is_enabled'),
                                   'expire_at', 'is_featured']}),
    ]

    change_list_template = 'backslash/change_list.html'

    class Meta(object):
        model = MenuItem

    def get_queryset(self, request, *args, **kwargs):
        queryset = super(MenuItemBackslash, self).get_queryset(request, *args,
                                                               **kwargs)
        if settings.SITE_FILTER:
            queryset = queryset.filter(Q(site__isnull=True) |
                                       Q(site=get_current_site(request)))
        return queryset.filter(parent=None)

    def change_view(self, request, object_id, form_url='', extra_content=None):
        # Use a custom view to manage the menu items completely
        # separately from Django's admin app.
        from .views import ManageMenuView
        view = ManageMenuView.as_view()
        response = view(request, pk=object_id, admin=self)
        if hasattr(response, 'render') and callable(response.render):
            return response.render()
        return response
