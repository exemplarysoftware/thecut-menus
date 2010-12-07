from django import template
from django.core.urlresolvers import NoReverseMatch, resolve, reverse


register = template.Library()


@register.inclusion_tag('admin/menus/menu/_menu.html', takes_context=True)
def menu(context, menu, extra_class=None):
    current_app = context.get('current_app', 'admin')
    return {'menu': menu, 'extra_class': extra_class,
        'current_app': current_app}


@register.simple_tag
def admin_object_change_url(admin_site, app_label, model_name,
    object_id):
    
    try:
        url = reverse(
            '%(admin_site)s:%(app_label)s_%(model_name)s_change' %({
            'admin_site': admin_site, 'app_label': app_label,
            'model_name': model_name}), args=[object_id])
    except NoReverseMatch:
        return '#'
    else:
        return url

