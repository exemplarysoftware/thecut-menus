from django import template
from django.contrib.contenttypes.models import ContentType
from thecut.menus.models import Menu, MenuItem


register = template.Library()

@register.inclusion_tag('menus/_menu.html', takes_context=True)
def menu(context, slug, extra_class=None):
    try:
        menu = Menu.objects.active().get(slug=slug)
    except Menu.DoesNotExist:
        menuitem_list = None
    else:
        menuitem_list = menu.items.active().select_generic_related()
    
    return {'menuitem_list': menuitem_list, 'extra_class': extra_class,
        'request': context.get('request')}


@register.inclusion_tag('menus/_menu.html', takes_context=True)
def section_menu(context, obj, extra_class=None):
    """Find a Menu which contains a MenuItem linking to this object.
    
    A rather crude way of finding a menu, which is determined by
    looking for the first MenuItem which links to this object.
    
    """
    content_type = ContentType.objects.get_for_model(obj)
    matching_menuitems = MenuItem.objects.active().filter(
        content_type=content_type, object_id=obj.pk)
    
    menuitem_list = matching_menuitems and \
        matching_menuitems[0].menu.items.active().select_generic_related() or \
        None
    
    return {'menuitem_list': menuitem_list, 'extra_class': extra_class,
        'request': context.get('request')}

