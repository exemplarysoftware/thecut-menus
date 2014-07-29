# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from model_utils.managers import PassThroughManagerMixin
from thecut.menus import querysets
from thecut.ordering.models import OrderMixin
from thecut.publishing.models import PublishableResource
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from . import managers


try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    from thecut.publishing.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class MenuItemContentType(ContentType):

    objects = managers.MenuItemContentTypeManager()

    class Meta(object):
        proxy = True

    def __str__(self):
        return self.name.title()


class PassThroughTreeManager(PassThroughManagerMixin, TreeManager):

    pass


@python_2_unicode_compatible
class MenuItem(MPTTModel, OrderMixin, PublishableResource):
    """An ordered item in a menu.

    If it is not the root of a menu or sub-menu, it is linked to
    another resource.

    """

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/menus', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    # Generic relation to an object.
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.IntegerField(db_index=True, blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = PassThroughTreeManager().for_queryset_class(
        querysets.MenuItemQuerySet)()

    class Meta(MPTTModel.Meta, PublishableResource.Meta):
        verbose_name = 'menu'
        verbose_name_plural = 'menus'

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
    """A django view, for potential use in menu items.

    """

    name = models.CharField(max_length=100)
    view = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        args = self.view.split()
        view_name = args.pop()
        return reverse(view_name, args=args)


@python_2_unicode_compatible
class WebLink(PublishableResource):
    """A website link, for potential use in menu items.

    """

    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
