# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.menus.templatetags.menu_tags import menu
from thecut.menus.tests.factories import MenuItemFactory, ViewLinkFactory
from django.test import TestCase
from django.test import Client
from thecut.menus.validators import validate_view
from django.core.exceptions import ValidationError
from thecut.menus.fields import MenuItemGenericForeignKey
from thecut.menus.models import MenuItemContentType


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
        self.assertEquals(response.content, b"Hello World")

    def test_reverse_links_to_the_correct_URL_with_parameters(self):
        viewlink = ViewLinkFactory(view='hello:world2 1111 2222')
        self.assertEquals(viewlink.get_absolute_url(),
                          '/hello/world2/1111/2222/')
        client = Client()
        response = client.get(viewlink.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, b"Hello World2 1111 2222")

    def test_validator_passes_correctly_on_a_simple_reverse_url(self):
        try:
            validate_view('hello:world')
        except:
            self.fail("validate_view() raised ValidationError unexpectedly!")

    def test_validator_fails_correctly_on_a_simple_reverse_url(self):
        with self.assertRaises(ValidationError):
            validate_view('hello:planet')

    def test_validator_passes_correctly_on_a_parameterised_reverse_url(self):
        try:
            validate_view('hello:world2 1111 2222')
        except:
            self.fail("validate_view() raised ValidationError unexpectedly!")

    def test_validator_errors_on_non_existing_params(self):
        with self.assertRaises(ValidationError):
            validate_view('hello:world 1111 2222')

    def test_validator_errors_on_insufficient_existing_params(self):
        with self.assertRaises(ValidationError):
            validate_view('hello:world2 1111')

    def test_validator_errors_on_invalid_params(self):
        with self.assertRaises(ValidationError):
            validate_view('hello:world2 1111 2a22')


class TestMenuItemFieldContentTypes(TestCase):
    # Test everything in the fields file
    def test_check_content_type_field_is_empty(self):
        f = MenuItemGenericForeignKey()
        self.assertTrue(len(f._check_content_type_field()) == 0)


class TestMenuItemContentType(TestCase):
    # Test we actually have some content types
    def test_menu_item_content_types_exit(self):
        queryset = MenuItemContentType.objects.all()
        self.assertTrue(len(queryset) > 0)
        names = set([str(ct) for ct in queryset])
        self.assertTrue('Internal Link' in names)
        self.assertTrue('External Link' in names)

    def test_menu_item_contenttypes_if_fresh_query_forced(self):
        MenuItemContentType.objects._menus_queryset = None
        queryset = MenuItemContentType.objects.all()
        self.assertTrue(len(queryset) > 0)
