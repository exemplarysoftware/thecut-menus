# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from django.conf.urls import include, patterns, url
from rest_framework.urlpatterns import format_suffix_patterns


urls = patterns(
    'thecut.menus.api.views',

    url(r'^$', views.MenusRootAPIView.as_view(), name='root'),

    url(r'^contenttypes/$',
        views.ContentTypeListAPIView.as_view(), name='contenttype_list'),

    url(r'^contenttypes/(?P<pk>\d+)/$',
        views.ContentTypeRetrieveAPIView.as_view(), name='contenttype_detail'),

    url(r'^menuitems/$',
        views.MenuItemListCreateAPIView.as_view(), name='menuitem_list'),

    url(r'^menuitems/(?P<pk>\d+)/$',
        views.MenuItemRetrieveAPIView.as_view(), name='menuitem_detail'),

    url(r'^menuitems/(?P<target_pk>\d+)/reorder/$',
        views.MenuItemMoveAPIView.as_view(), name='menuitem_move'),

)

urlpatterns = patterns(
    '', (r'^', include(urls, namespace='menus_menuitem_api')))

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
