# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut import backslash
from .admin import MenuItemAdmin
from .forms import MenuItemBackslashForm
from .models import MenuItem


class MenuItemBackslash(MenuItemAdmin, backslash.ModelAdmin):
    """Add and a top-level root MenuItem and manage it's children."""

    form = MenuItemBackslashForm

    fieldsets = [
        (None, {'fields': ['title', 'slug']}),
        ('Publishing', {'fields': [('publish_at', 'is_enabled'),
                                   'expire_at']}),
    ]

    change_list_template = 'backslash/change_list.html'

    class Meta(object):
        model = MenuItem

    def get_queryset(self, *args, **kwargs):
        queryset = super(MenuItemBackslash, self).get_queryset(*args, **kwargs)
        # Only display top-level menus for editing in backslash.
        return queryset.filter(object_id__isnull=True, parent__isnull=True)

    def change_view(self, request, object_id, form_url='', extra_content=None):
        # Use a custom view to manage the menu items completely
        # separately from Django's admin app.
        from .views import ManageMenuView
        view = ManageMenuView.as_view()
        response = view(request, pk=object_id, admin=self)
        if hasattr(response, 'render') and callable(response.render):
            return response.render()
        return response
