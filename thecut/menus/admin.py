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


class MenuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Publishing', {'fields': ['slug', ('publish_at', 'is_enabled')],
            'classes': ['collapse']}),
    ]
    form = MenuAdminForm
    inlines = [MenuItemInline]
    prepopulated_fields = {'slug': ['name']}
    
    def get_urls(self):
        urlpatterns = patterns('menus.views',
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
admin.site.register(ViewLink, ViewLinkAdmin)
admin.site.register(WebLink, WebLinkAdmin)

