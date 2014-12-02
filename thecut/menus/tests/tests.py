# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.menus.templatetags.menu_tags import menu
from thecut.menus.tests.factories import MenuItemFactory
from django.test import TestCase


class TestMenuTag(TestCase):

    def setUp(self):
        self.root = MenuItemFactory(slug='root')
        self.child = MenuItemFactory(parent=self.root)

    def test_returns_a_menuitems_children_when_given_a_slug(self):

        result = menu({}, 'root')

        self.assertIn(self.child, result['menuitem_list'])

    def test_returns_a_menuitems_children_when_given_a_menuitem(self):

        result = menu({}, self.root)

        self.assertIn(self.child, result['menuitem_list'])
