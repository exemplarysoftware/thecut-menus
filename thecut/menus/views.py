# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import MenuItem
from django.views import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode


class ManageMenuView(generic.DetailView):

    model = MenuItem

    template_name = 'backslash/menus/menuitem_detail.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(ManageMenuView, self).get_context_data(*args,
                                                                    **kwargs)
        admin = self.kwargs['admin']
        opts = admin.model._meta
        content_type = ContentType.objects.get_for_model(admin.model)
        defaults = {'current_app': admin.admin_site.name, 'opts': opts,
                    'app_label': opts.app_label, 'add': False,
                    'content_type': content_type, 'form_url': '',
                    'title': 'Add {0}'.format(
                        force_unicode(opts.verbose_name_plural)),
                    'root_path': getattr(admin.admin_site, 'root_path', None),
                    'media': '',
                    'errors': None,
                    'change': False, 'is_popup': False, 'save_as': False,
                    'save_on_top': False, 'show_delete': False,
                    'has_file_field': False, 'has_add_permission': False,
                    'has_change_permission': False,
                    'has_delete_permission': False,
                    'content_type_id': content_type.id,
                    'change_form_template': '{0}/menuitem_form.html'.format(
                        admin.admin_site.name),
                    }

        for key, value in defaults.items():
            context_data.setdefault(key, value)

        return context_data

    def render_to_response(self, *args, **kwargs):
        admin = self.kwargs['admin']
        current_app = admin.admin_site.name
        return super(ManageMenuView, self).render_to_response(
            *args, current_app=current_app, **kwargs)
