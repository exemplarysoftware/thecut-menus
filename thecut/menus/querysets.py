# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models
from thecut.publishing.querysets import PublishableResourceQuerySet
import warnings


class MenuItemQuerySet(PublishableResourceQuerySet):

    def active(self, *args, **kwargs):
        """Return active (enabled, published) objects which are linked to an object.

        """

        queryset = super(MenuItemQuerySet, self).active(*args, **kwargs)
        return queryset.exclude(models.Q(content_type__isnull=True) |
                                models.Q(object_id__isnull=True))

    def prefetch_content_objects(self):
        """Attempt to prefetch related content objects, if available.

        """

        # The prefetch_related is only available in Django 1.4+
        if hasattr(self, 'prefetch_related'):
            queryset = self.prefetch_related('content_object')
        else:
            queryset = self.select_generic_related()

        return queryset

    def select_generic_related(self):
        # Deprecated method, will be removed as this functionality is now
        # covered by prefetch_related since Django 1.4.
        warnings.warn('select_generic_related is deprecated - use '
                      'prefetch_related (available in Django 1.4+) instead.',
                      DeprecationWarning, stacklevel=2)
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
