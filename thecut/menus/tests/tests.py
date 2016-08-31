# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.menus.templatetags.menu_tags import menu, section_menu
from thecut.menus.tests.factories import (MenuItemFactory, ViewLinkFactory,
                                          WebLinkFactory)
from django.test import TestCase
from django.test import Client
from thecut.menus.validators import validate_view
from django.core.exceptions import ValidationError
from thecut.menus.fields import MenuItemGenericForeignKey
from thecut.menus.models import MenuItemContentType, ViewLink
from mock import patch, PropertyMock


class TestMenuTag(TestCase):

    def setUp(self):
        self.root = MenuItemFactory(slug='root')
        self.child = MenuItemFactory(parent=self.root)
        self.secondchild = MenuItemFactory(parent=self.root
                                           )
        viewlink = ViewLinkFactory(view='hello:world')
        viewlink_content_type = [ct for ct in MenuItemContentType.objects.all()
                                 if ct.name == ViewLink._meta.verbose_name][0]
        self.secondchild.content_type = viewlink_content_type
        self.secondchild.object_id = viewlink.id

    def test_returns_a_menuitems_children_when_given_a_slug(self):

        result = menu({}, 'root')

        self.assertIn(self.child, result['menuitem_list'])
        self.assertEquals(result['level'], 1)

    def test_returns_a_menuitems_children_when_given_a_menuitem(self):

        result = menu({}, self.root)

        self.assertIn(self.child, result['menuitem_list'])

    def test_menuitem_string_cast_returns_title(self):
        result = str(self.child)
        self.assertEqual(result, self.child.title)
        self.assertRegexpMatches(result, 'Menu Item [\d]')

    def test_menuitem_returns_contents_url(self):
        viewlink = ViewLinkFactory(view='hello:world')
        self.assertEquals(self.secondchild.get_absolute_url(),
                          viewlink.get_absolute_url())
        self.assertEquals(self.child.get_absolute_url(), None)

    def test_menuitem_css_classes(self):
        self.assertEqual(self.secondchild.get_css_classes(), '')
        self.assertEqual(self.root.get_css_classes(), 'has-menu')
        self.child.is_featured = True
        self.assertRegexpMatches(self.child.get_css_classes(), 'featured')
        with patch('thecut.menus.models.MenuItem.image',
                   new_callable=PropertyMock) as mock_image:
            mock_image.return_value = True
            self.assertRegexpMatches(self.child.get_css_classes(), 'has-image')

    def test_returns_empty_list_when_given_an_invalid_slug(self):

        result = menu({}, 'invalidslug')

        self.assertEqual(len(result['menuitem_list']), 0)

    def test_level_correctly(self):

        result = menu({}, 'root', level=1)

        self.assertIn(self.child, result['menuitem_list'])
        self.assertEquals(result['level'], 2)


class TestSectionMenuTag(TestCase):

    def setUp(self):
        self.root = MenuItemFactory(slug='root')
        self.child = MenuItemFactory(parent=self.root)
        self.secondchild = MenuItemFactory(parent=self.root
                                           )
        self.viewlink = ViewLinkFactory(view='hello:world')
        viewlink_content_type = [ct for ct in MenuItemContentType.objects.all()
                                 if ct.name == ViewLink._meta.verbose_name][0]
        self.secondchild.content_type = viewlink_content_type
        self.secondchild.object_id = self.viewlink.id
        self.secondchild.save()

    def test_returns_menuitems_when_given_a_model(self):

        result = section_menu({}, self.viewlink)

        self.assertIn(self.secondchild, result['menuitem_list'])

    def test_returns_no_menuitems_when_given_an_unlinked_model(self):
        viewlink2 = ViewLinkFactory(view='hello:world2 1111 2222')
        result = section_menu({}, viewlink2)

        self.assertEqual(len(result['menuitem_list']), 0)


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

    def test_casting_viewlink_to_string(self):
        viewlink = ViewLinkFactory(view='hello:world')
        self.assertEquals(viewlink.name, str(viewlink))

    def test_reverse_links_to_invalid_URL_is_none(self):
        viewlink = ViewLinkFactory(view='hello:world3 1111 2222')
        self.assertEquals(viewlink.get_absolute_url(), None)


class TestWeblinks(TestCase):
    def setUp(self):
        self.weblink = WebLinkFactory(url='www.thecut.net.au')

    def test_weblink_names(self):
        self.assertEqual(self.weblink.name, str(self.weblink))

    def test_weblink_url(self):
        self.assertEqual(self.weblink.url, self.weblink.get_absolute_url())


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
