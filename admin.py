from django.contrib import admin
from menus.models import MenuItem, Menu, ViewLink, WebLink


class MenuItemInline(admin.TabularInline):
    exclude = ['is_featured', 'publish_at', 'publish_by', 'title']
    extra = 0
    model = MenuItem


class MenuAdmin(admin.ModelAdmin):
    exclude = ['is_featured', 'publish_by']
    inlines = [MenuItemInline]
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class ViewLinkAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class WebLinkAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if not change: obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


admin.site.register(Menu, MenuAdmin)
admin.site.register(ViewLink, ViewLinkAdmin)
admin.site.register(WebLink, WebLinkAdmin)

