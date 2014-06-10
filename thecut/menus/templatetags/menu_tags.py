# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import template
from django.contrib.contenttypes.models import ContentType
from thecut.menus.models import MenuItem


register = template.Library()


@register.inclusion_tag('menus/_menu.html', takes_context=True)
def menu(context, slug_or_menuitem, extra_class=None):

    menu = None

    if type(slug_or_menuitem) == MenuItem:
        menu = slug_or_menuitem
    else:

        try:
            menu = MenuItem.objects.active().get(slug=slug_or_menuitem)
        except MenuItem.DoesNotExist:
            menu = None

    # TODO: menu.children.active().prefetch_content_objects()
    menuitem_list = menu.children.active() if menu else []

    return {'menuitem_list': menuitem_list, 'extra_class': extra_class,
            'request': context.get('request')}


@register.inclusion_tag('menus/_menu.html', takes_context=True)
def section_menu(context, obj, extra_class=None):
    """Find a MenuItem linking to this object.

    A rather crude way of finding a menu, which is determined by
    looking for the first MenuItem which links to this object.

    """
    content_type = ContentType.objects.get_for_model(obj)
    matching_menuitems = MenuItem.objects.active().filter(
        content_type=content_type, object_id=obj.pk)[:1]

    if matching_menuitems:
        menu = matching_menuitems[0].parent
        menuitem_list = menu.items.active().prefetch_content_objects()
    else:
        menuitem_list = None

    return {'menuitem_list': menuitem_list, 'extra_class': extra_class,
            'request': context.get('request')}
