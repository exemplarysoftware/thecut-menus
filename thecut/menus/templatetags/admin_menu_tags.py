from django import template


register = template.Library()


@register.inclusion_tag('admin/menus/menu/_menu.html')
def menu(menu, extra_class=None):
    return {'menu': menu, 'extra_class': extra_class}

