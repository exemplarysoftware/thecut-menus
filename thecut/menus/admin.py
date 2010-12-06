from datetime import datetime
from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from thecut.menus.forms import MenuAdminForm, MenuItemAdminForm, ViewLinkAdminForm, WebLinkAdminForm
from thecut.menus.models import MenuItem, Menu, ViewLink, WebLink


class MenuItemInline(admin.StackedInline):#admin.options.InlineModelAdmin):
    extra = 0
    fields = ['name', 'order', 'content_type', 'object_id']
    form = MenuItemAdminForm
    model = MenuItem
    #template = 'admin/menus/edit_inline/menuitem_inline.html'


class OldMenuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Publishing', {'fields': ['slug', ('publish_at', 'is_enabled')],
            'classes': ['collapse']}),
    ]
    form = MenuAdminForm
    inlines = [MenuItemInline]
    prepopulated_fields = {'slug': ['name']}
    
    def get_urls(self):
        urlpatterns = patterns('thecut.menus.views',
            url(r'^menuitem/contenttype/(?P<content_type_pk>\d+)/$',
                'menuitem_admin_contenttype_list',
                name='menuitem_admin_contenttype_list'),
        )
        urlpatterns += super(MenuAdmin, self).get_urls()
        return urlpatterns
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()
    
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


class MenuAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'publish_at']
    #change_form_template = 'menus/admin/change_form.html'
    #def changelist_view(self, request, extra_context=None):
    
    class Media:
        css = {'all': ['menus/admin.css']}
        js = ['menus/jquery.min.js', 'menus/jquery-ui.min.js', 'menus/admin.js']
    
    def get_urls(self):
        urlpatterns = patterns('thecut.menus.views',
            url(r'^(?P<menu_pk>\d+)/add-child$',
                'menu_admin_add_child',
                name='menus_menu_admin_add_child'),
            url(r'^menuitem/reorder$',
                'menuitem_admin_reorder',
                name='menus_menuitem_admin_reorder'),
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


class MenuItemAdmin(admin.ModelAdmin):
    fields = ['name', 'content_type', 'object_id', 'is_enabled']


class ViewLinkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'view']}),
        ('Publishing', {'fields': [('publish_at', 'is_enabled')],
            'classes': ['collapse']}),
    ]
    form = ViewLinkAdminForm
    list_display = ['name', 'view']
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class WebLinkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'url']}),
        ('Publishing', {'fields': [('publish_at', 'is_enabled')],
            'classes': ['collapse']}),
    ]
    form = WebLinkAdminForm
    list_display = ['name', 'url']
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(ViewLink, ViewLinkAdmin)
admin.site.register(WebLink, WebLinkAdmin)

