# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from thecut.publishing.querysets import PublishableResourceQuerySet


class MenuItemQuerySet(PublishableResourceQuerySet):
    """Customised :py:class:`~django.db.models.db.query.QuerySet` for
    :py:class:`~thecut.menus.models.MenuItem` model."""

    def prefetch_content_objects(self):
        """Prefetch the related content objects."""
        return self.prefetch_related('content_object')
