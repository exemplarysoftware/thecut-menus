# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework import permissions


class MenuItemAPIPermissions(permissions.DjangoModelPermissions):
    """Permissions required to access the APIs for managing menus."""

    permission_string = 'menus.change_menuitem'
    perms_map = {
        'GET': [permission_string],
        'OPTIONS': [permission_string],
        'HEAD': [permission_string],
        'POST': [permission_string],
        'PUT': [permission_string],
        'PATCH': [permission_string],
        'DELETE': [permission_string],
    }
