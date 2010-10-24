from django import template
from menus.models import Menu


register = template.Library()

@register.inclusion_tag('menus/_menu.html', takes_context=True)
def menu(context, slug, extra_class=None):
    try:
        menu = Menu.objects.active().get(slug=slug)
    except Menu.DoesNotExist:
        menu = None
    request = context['request']
    return {'menu': menu, 'extra_class': extra_class,
        'request': request}

