# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from django.conf.urls import include, patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


urls = patterns(
    'thecut.menus.api.views',
    url(r'^$', views.RootAPIView.as_view(), name='root'),

    url(r'^contenttypes/$',
        views.ContentTypeListAPIView.as_view(), name='contenttype_list'),

    url(r'^contenttypes/(?P<pk>\d+)/$',
        views.ContentTypeRetrieveAPIView.as_view(), name='contenttype_detail'),

    url(r'^menuitems/$',
        views.MenuItemListAPIView.as_view(), name='menuitem_list'),

)

urlpatterns = patterns(
    '',
    (r'^', include(urls, namespace='menus_menuitem_api')))
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
