# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from django.contrib.contenttypes.models import ContentTypeManager
from django.db.models import Q
from model_utils.managers import PassThroughManagerMixin
from mptt.managers import TreeManager
import operator


class MenuItemContentTypeManager(ContentTypeManager):

    _queryset = None

    def get_queryset(self, *args, **kwargs):
        queryset = super(MenuItemContentTypeManager, self).get_queryset(
            *args, **kwargs)

        # Evaluate the queryset and store it on the class
        if MenuItemContentTypeManager._queryset is None:
            # Convert 'app.Model' strings in to (app_label, model) tuples.
            models = (
                ('.'.join(model.split('.')[:-1]), model.split('.')[-1]) for
                model in settings.SELECTABLE_MODELS)
            # Construct query to filter for ContentType objects which match the
            # app_label and model combinations.
            query = reduce(operator.or_, (Q(app_label__iexact=app_label,
                                            model__iexact=model)
                                          for app_label, model in models))
            queryset = queryset.filter(query)
            MenuItemContentTypeManager._queryset = queryset

        return MenuItemContentTypeManager._queryset


class PassThroughTreeManager(PassThroughManagerMixin, TreeManager):

    pass
