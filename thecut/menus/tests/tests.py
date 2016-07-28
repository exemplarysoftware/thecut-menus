# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.menus.templatetags.menu_tags import menu
from thecut.menus.tests.factories import MenuItemFactory, ViewLinkFactory
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from thecut.menus.validators import validate_view


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


class TestViewLinkReverse(TestCase):
    # We test reversing the URL and passing parameter via a reversed URl

    def test_reverse_links_to_the_correct_URL_without_parameters(self):
        viewlink = ViewLinkFactory(view='hello:world')
        self.assertEquals(viewlink.get_absolute_url(), '/hello/world/')
        client = Client()
        response = client.get(viewlink.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "Hello World")

    #def test_reverse_links_to_the_correct_URL_with_parameters(self):
    #    url = reverse('hello:world2 1111 2222')
    #    self.assertEquals(url, '/hello/world2/1111/2222/')
    #    response = client.get(url)
    #    self.assertEquals(response.status_code, 200)
    #    self.assertEquals(response.content, "Hello world2 1111 2222")

    #def test_validator_passes_correctly_on_a_simple_reverse_url(self):
    #    try:
    #        validate_view('hello:world')
    #    except:
    #        self.fail("validate_view() raised ValidationError unexpectedly!")

    #def test_validator_fails_correctly_on_a_simple_reverse_url(self):
    #    self.assertRaises(ValidationError, validate_view('hello:planet'))

    #def test_validator_passes_correctly_on_a_parameterised_reverse_url(self):
    #    try:
    #        validate_view('hello:world2 1111 2222')
    #    except:
    #        self.fail("validate_view() raised ValidationError unexpectedly!")

    #def test_validator_does_not_know_url_expects_params_always_allows(self):
    #    try:
    #        validate_view('hello:world 1111 2222')
    #    except:
    #        self.fail("validate_view() raised ValidationError unexpectedly!")


