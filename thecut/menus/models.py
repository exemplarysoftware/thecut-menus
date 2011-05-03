from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from thecut.core.managers import QuerySetManager
from thecut.core.models import AbstractBaseResource


class Menu(AbstractBaseResource):
    """A collection of menu items."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    objects = QuerySetManager()
    
    def __unicode__(self):
        return self.name
    
    @property
    def menuitem_set(self):
        """Deprecated - instead use 'items()'."""
        warnings.warn('menuitem_set property is deprecated - use '
            '\'items\' property.', DeprecationWarning,
            stacklevel=2)
        return self.items


class MenuItem(AbstractBaseResource):
    """Links a Menu to an object, and provides an order."""
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    menu = models.ForeignKey('Menu', related_name='items')
    
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
        
        def select_generic_related(self):
            queryset = self.all()
            
            # Simulating select_related() on GenericForeignKey
            # http://blog.roseman.org.uk/2010/02/22/django-patterns-part-4-forwards-generic-relations/
            generics = {}
            for item in queryset:
                if item.content_type_id:
                    generics.setdefault(item.content_type_id, set()).add(
                        item.object_id)
            
            content_types = ContentType.objects.in_bulk(generics.keys())
            
            relations = {}
            for ct, fk_list in generics.items():
                ct_model = content_types[ct].model_class()
                relations[ct] = ct_model.objects.in_bulk(list(fk_list))
            
            for item in queryset:
                if item.content_type_id and item.object_id:
                    try:
                        setattr(item, '_content_object_cache',
                            relations[item.content_type_id][item.object_id])
                    except KeyError:
                        pass
            
            return queryset
    
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

