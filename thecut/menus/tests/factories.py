# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.menus.models import MenuItem
import factory
from django import VERSION

if VERSION > (1, 5):
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
else:
    from django.contrib.auth.models import User
    user_model = User


class UserFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = user_model
    FACTORY_DJANGO_GET_OR_CREATE = ('username', )

    username = factory.Sequence(lambda n: 'user_{}@example.com'.format(n))


class MenuItemFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = MenuItem
    FACTORY_DJANGO_GET_OR_CREATE = ('slug', )

    name = factory.Sequence(lambda n: 'Menu Item {0}'.format(n))
    slug = 'default-menu-item'
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
