from django import template
from menus.models import Menu

register = template.Library()

@register.inclusion_tag('menus/_menu.html')
def menu(slug, extra_class=None):
    print slug
    try:
        menu = Menu.objects.active().get(slug=slug)
    except Menu.DoesNotExist:
        menu = None
    return {'menu': menu, 'extra_class': extra_class}

