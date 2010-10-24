from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from thecut.managers import QuerySetManager
from thecut.models import AbstractBaseResource


class Menu(AbstractBaseResource):
    """A collection of menu items."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    objects = QuerySetManager()
    
    def __unicode__(self):
        return self.name


class MenuItem(AbstractBaseResource):
    """Links a Menu to an object, and provides an order."""
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    menu = models.ForeignKey('Menu')
    
    # Generic relation to an object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = QuerySetManager()
    
    class Meta(AbstractBaseResource.Meta):
        ordering = ['order']
    
    def __unicode__(self):
        return self.name or str(self.content_object)
    
    def get_absolute_url(self):
        return self.content_object.get_absolute_url()
    
    @property
    def is_menu(self):
        return isinstance(self.content_object, Menu)


class ViewLink(AbstractBaseResource):
    """A django view, for potential use in menu items."""
    name = models.CharField(max_length=100)
    view = models.CharField(max_length=100)
    
    objects = QuerySetManager()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(self.view)


class WebLink(AbstractBaseResource):
    """A website link, for potential use in menu items."""
    name = models.CharField(max_length=100)
    url = models.URLField()
    
    objects = QuerySetManager()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.url

