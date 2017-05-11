# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import managers, querysets
from .fields import MenuItemGenericForeignKey
from .validators import validate_view
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from thecut.ordering.models import OrderMixin
from thecut.publishing.models import PublishableResource


@python_2_unicode_compatible
class MenuItemContentType(ContentType):

    objects = managers.MenuItemContentTypeManager()

    class Meta(object):
        proxy = True

    def __str__(self):
        return self.name.title()


@python_2_unicode_compatible
class MenuItem(MPTTModel, OrderMixin, PublishableResource):
    """An ordered item in a menu.

    If it is not the root of a menu or sub-menu, it is linked to
    another resource.

    """

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    title = models.CharField(max_length=200, blank=True)

    image = models.ImageField(upload_to='uploads/menus', blank=True)

    slug = models.SlugField(unique=True, null=True)

    content_type = models.ForeignKey('menus.MenuItemContentType', blank=True,
                                     null=True, related_name='+',
                                     on_delete=models.CASCADE)

    object_id = models.IntegerField(db_index=True, blank=True, null=True)

    content_object = MenuItemGenericForeignKey('content_type', 'object_id')

    objects = TreeManager.from_queryset(querysets.MenuItemQuerySet)()

    site = models.ForeignKey('sites.Site', blank=True, null=True,
                             related_name='+', on_delete=models.SET_NULL)

    class Meta(MPTTModel.Meta, PublishableResource.Meta):
        verbose_name = 'menu'
        verbose_name_plural = 'menus'

    class MPTTMeta(object):
        order_insertion_by = ['order']

    def __str__(self):
        return '{0}'.format(self.title or self.content_object)

    def get_absolute_url(self):
        if not self.is_menu():
            return self.content_object.get_absolute_url()

    def get_css_classes(self):
        css_classes = ['featured' if self.is_featured else '',
                       'has-image' if self.image else '',
                       'has-menu' if self.is_menu() else '']
        return ' '.join(filter(bool, css_classes))

    def is_menu(self):
        return self.content_object is None


@python_2_unicode_compatible
class ViewLink(PublishableResource):
    """A django view, for potential use in menu items."""

    name = models.CharField(max_length=100, help_text='Friendly display name.')

    view = models.CharField(max_length=100,
                            validators=[validate_view],
                            help_text='Django view URL name to resolve. '
                            'Format view:link arg1 arg2')

    class Meta(PublishableResource.Meta):
        verbose_name = 'Internal link'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        args = self.view.split()
        try:
            url = reverse(args[0], args=args[1:])
        except NoReverseMatch:
            url = None
        return url


@python_2_unicode_compatible
class WebLink(PublishableResource):
    """A website link, for potential use in menu items."""

    name = models.CharField(max_length=100)

    url = models.URLField()

    class Meta(PublishableResource.Meta):
        verbose_name = 'External link'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
