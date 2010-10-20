from datetime import datetime
from django import forms
from menus.models import Menu, ViewLink, WebLink


class MenuAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuAdminForm, self).__init__(*args, **kwargs)
        self.fields['publish_at'].initial = datetime.now()
    
    class Meta:
        model = Menu


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

