# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.menus.models import MenuItem, ViewLink
import factory
from django.contrib.auth import get_user_model
user_model = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = user_model
        django_get_or_create = ('username', )

    username = factory.Sequence(lambda n: 'user_{0}@example.com'.format(n))


class MenuItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MenuItem
        django_get_or_create = ('slug', )

    title = factory.Sequence(lambda n: 'Menu Item {0}'.format(n))
    slug = 'default-menu-item'
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)


class ViewLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ViewLink

    name = factory.Sequence(lambda n: 'View Link {0}'.format(n))
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
