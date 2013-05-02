# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from thecut.authorship.admin import AuthorshipMixin
from thecut.menus.forms import (MenuAdminForm, MenuItemAdminForm,
                                MenuItemInlineForm, ViewLinkAdminForm,
                                WebLinkAdminForm)
from thecut.menus.models import MenuItem, Menu, ViewLink, WebLink


class MenuItemInline(admin.TabularInline):

    extra = 0
    fields = ('name', 'order', 'content_type', 'object_id')
    form = MenuItemInlineForm
    model = MenuItem


class StandardMenuAdmin(AuthorshipMixin, admin.ModelAdmin):

    change_form_template = 'admin/menus/menu/change_form_old.html'
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Publishing', {'fields': ('slug', ('publish_at', 'is_enabled'),
                                   'is_featured'),
                        'classes': ('collapse',)}),
    )
    form = MenuAdminForm
    inlines = (MenuItemInline,)
    prepopulated_fields = {'slug': ('name',)}

    def get_urls(self):
        urlpatterns = patterns('thecut.menus.views',
            url(r'^menuitem/contenttype/$',
                'menuitem_admin_contenttype_list',
                name='menus_menuitem_admin_contenttype_list'),
            url(r'^menuitem/contenttype/(?P<content_type_pk>\d+)/$',
                'menuitem_admin_contenttype_object_list',
                name='menus_menuitem_admin_contenttype_object_list'),
        )
        urlpatterns += super(StandardMenuAdmin, self).get_urls()
        return urlpatterns

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.created_by = request.user
            instance.updated_by = request.user
            if not instance.publish_at:
                instance.publish_at = datetime.now()
            instance.save()
        #formset.save()


admin.site.register(Menu, StandardMenuAdmin)


class MenuAdmin(AuthorshipMixin, admin.ModelAdmin):

    fields = ('name', 'slug', 'publish_at', 'is_featured')
    ordering = ('-is_featured',)

    class Media:
        css = {'all': ['menus/fancybox/jquery.fancybox-1.3.4.css',
                       'menus/admin.css']}
        js = ['menus/jquery.min.js', 'menus/jquery-ui.min.js',
              'menus/jquery.form.js',
              'menus/fancybox/jquery.fancybox-1.3.4.pack.js',
              'menus/admin.js', 'menus/csrf.js']

    def change_view(self, *args, **kwargs):
        # Set 'current_app' to name of admin site.
        extra_context = kwargs.pop('extra_context', {})
        extra_context.update({'current_app': self.admin_site.name})
        return super(MenuAdmin, self).change_view(*args,
            extra_context=extra_context, **kwargs)

    def changelist_view(self, request, *args, **kwargs):
        # Remove add menu link from change list if not a superuser.
        extra_context = kwargs.pop('extra_context', {})
        if not request.user.is_superuser:
            extra_context.update({'has_add_permission': False})
        return super(MenuAdmin, self).changelist_view(
            request, *args, extra_context=extra_context, **kwargs)

    def queryset(self, request):
        queryset = super(MenuAdmin, self).queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(is_featured=True)

    def get_urls(self):
        urlpatterns = patterns('thecut.menus.views',
            url(r'^(?P<menu_pk>\d+)/add-child$',
                'menu_admin_add_child',
                name='menus_menu_admin_add_child'),

            url(r'^menuitem/reorder$',
                'menuitem_admin_reorder',
                name='menus_menuitem_admin_reorder'),
            url(r'^menuitem/contenttype/$',
                'menuitem_admin_contenttype_list',
                name='menus_menuitem_admin_contenttype_list'),
            url(r'^menuitem/contenttype/(?P<content_type_pk>\d+)/$',
                'menuitem_admin_contenttype_object_list',
                name='menus_menuitem_admin_contenttype_object_list'),

            url(r'^(?P<menu_pk>\d+)/menuitem/add/placeholder$',
                'menuitem_admin_add_placeholder',
                name='menus_menu_menuitem_admin_add_placeholder'),
            url(r'^(?P<menu_pk>\d+)/menuitem/add$',
                'menuitem_admin_add',
                name='menus_menu_menuitem_admin_add'),
            url(r'^(?P<menu_pk>\d+)/menuitem/(?P<menuitem_pk>\d+)/edit$',
                'menuitem_admin_edit',
                name='menus_menu_menuitem_admin_edit'),
            url(r'^(?P<menu_pk>\d+)/menuitem/(?P<menuitem_pk>\d+)/delete$',
                'menuitem_admin_delete',
                name='menus_menu_menuitem_admin_delete'),
        )
        urlpatterns += super(MenuAdmin, self).get_urls()
        return urlpatterns


class MenuItemAdmin(AuthorshipMixin, admin.ModelAdmin):

    fields = ('name', 'content_type', 'object_id', 'is_enabled')

admin.site.register(MenuItem, MenuItemAdmin)


class ViewLinkAdmin(AuthorshipMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('name', 'view')}),
        ('Publishing', {'fields': (('publish_at', 'is_enabled'),),
                        'classes': ('collapse',)}),
    )
    form = ViewLinkAdminForm
    list_display = ('name', 'view')

admin.site.register(ViewLink, ViewLinkAdmin)


class WebLinkAdmin(AuthorshipMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('name', 'url')}),
        ('Publishing', {'fields': (('publish_at', 'is_enabled'),),
                        'classes': ('collapse',)}),
    )
    form = WebLinkAdminForm
    list_display = ('name', 'url')

admin.site.register(WebLink, WebLinkAdmin)
