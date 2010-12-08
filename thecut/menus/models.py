from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
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
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = QuerySetManager()
    
    class QuerySet(AbstractBaseResource.QuerySet):
        def active(self):
            """Return active (enabled, published) objects which are linked to an object."""
            queryset = super(MenuItem.QuerySet, self).active()
            return queryset.exclude(content_type__isnull=True).exclude(
                object_id__isnull=True)
    
    class Meta(AbstractBaseResource.Meta):
        ordering = ['order']
    
    def __unicode__(self):
        return self.name or str(self.content_object)
    
    def get_absolute_url(self):
        return self.content_object.get_absolute_url()
    
    @property
    def is_active(self):
        is_active = self in self.__class__.objects.active().filter(
            pk=self.pk)
        object_active = getattr(self.content_object, 'is_active', True)
        return object_active and is_active or False
    
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
    
    @models.permalink
    def get_absolute_url(self):
        args = self.view.split()
        view_name = args.pop(0)
        return (view_name, args)


class WebLink(AbstractBaseResource):
    """A website link, for potential use in menu items."""
    name = models.CharField(max_length=100)
    url = models.URLField()
    
    objects = QuerySetManager()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.url

