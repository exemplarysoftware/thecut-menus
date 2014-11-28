# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions


__all__ = ['MenuItemPermissions', 'IsAdminUser']


class MenuItemPermissions(DjangoModelPermissions):
    """Extended version of DjangoModelPermissions which checks for ``change``
    permissions for API requests."""

    perms_map = {
        'GET': ['menus.change_menuitem'],
        'OPTIONS': ['menus.change_menuitem'],
        'HEAD': ['menus.change_menuitem'],
        'POST': ['menus.change_menuitem'],
        'PUT': ['menus.change_menuitem'],
        'PATCH': ['menus.change_menuitem'],
        'DELETE': ['menus.change_menuitem'],
    }
