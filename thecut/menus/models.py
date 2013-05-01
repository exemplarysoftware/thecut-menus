# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.managers import PassThroughManager
from thecut.menus import querysets
from thecut.publishing.models import PublishableResource

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    from thecut.publishing.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class Menu(PublishableResource):
    """A collection of menu items.

    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class MenuItem(PublishableResource):
    """Links a Menu to an object, and provides an order.

    """

    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/menus', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    menu = models.ForeignKey('Menu', related_name='items')

    # Generic relation to an object.
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.IntegerField(db_index=True, blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = PassThroughManager().for_queryset_class(
        querysets.MenuItemQuerySet)()

    class Meta(PublishableResource.Meta):
        ordering = ('order',)

    def __str__(self):
        return '{0}'.format(self.name or self.content_object)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def get_css_classes(self):
        css_classes = ['featured' if self.is_featured else '',
                       'has-image' if self.image else '',
                       'has-menu' if self.is_menu() else '']
        return ' '.join(filter(bool, css_classes))

    def is_active(self, *args, **kwargs):
        item_active = super(MenuItem, self).is_active(*args, **kwargs)

        if item_active:
            object_active = getattr(self.content_object, 'is_active', True)
            if callable(object_active):
                object_active = object_active()
            return bool(object_active)
        else:
            return False

    def is_menu(self):
        return isinstance(self.content_object, Menu)


@python_2_unicode_compatible
class ViewLink(PublishableResource):
    """A django view, for potential use in menu items.

    """

    name = models.CharField(max_length=100)
    view = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        args = self.view.split()
        view_name = args.pop(0)
        return (view_name, args)


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
