from datetime import datetime
from django.contrib import admin
from menus.forms import MenuAdminForm, ViewLinkAdminForm, WebLinkAdminForm
from menus.models import MenuItem, Menu, ViewLink, WebLink


class MenuItemInline(admin.TabularInline):
    exclude = ['is_featured', 'publish_at', 'publish_by', 'title']
    extra = 0
    model = MenuItem


class MenuAdmin(admin.ModelAdmin):
    exclude = ['is_featured', 'publish_by']
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Publishing', {'fields': ['slug', ('publish_at', 'is_enabled')],
            'classes': ['collapse']}),
    ]
    form = MenuAdminForm
    inlines = [MenuItemInline]
    prepopulated_fields = {'slug': ['name']}
    
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

