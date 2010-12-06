from datetime import datetime
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from thecut.menus.models import Menu, MenuItem, ViewLink, WebLink


SELECTABLE_MODELS = getattr(settings, 'MENUS_SELECTABLE_MODELS',
    ['menus.Menu', 'menus.ViewLink', 'menus.WebLink'])


class MenuAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuAdminForm, self).__init__(*args, **kwargs)
        self.fields['publish_at'].initial = datetime.now()
    
    class Meta:
        model = Menu


class MenuItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].label = 'Target'
        self.fields['object_id'].label = 'Object'
        
        content_types = []
        for app_model in SELECTABLE_MODELS:
            app_label, model = app_model.lower().split('.')
            content_types += [ContentType.objects.get(
                app_label=app_label, model=model)]
        queryset = self.fields['content_type'].queryset
        self.fields['content_type'].queryset = queryset.filter(
            pk__in=[ct.pk for ct in content_types])
    
    class Media:
        css = {'all': ['menus/menuitem_inline.css']}
        js = ['javascripts/jquery.js', 'javascripts/jquery-ui.js',
            'menus/menuitem_inline.js']
    
    class Meta:
        model = MenuItem


class ViewLinkAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ViewLinkAdminForm, self).__init__(*args, **kwargs)
        self.fields['publish_at'].initial = datetime.now()
    
    class Meta:
        model = ViewLink


class WebLinkAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebLinkAdminForm, self).__init__(*args, **kwargs)
        self.fields['publish_at'].initial = datetime.now()
    
    class Meta:
        model = WebLink

