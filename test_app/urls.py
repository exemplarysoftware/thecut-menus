# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from . import views

urls = [
    url(r'^world/$', views.HelloWorldView.as_view(), name='world'),
    url(r'^world2/(\d{4})/(\d{4})/$', views.HelloWorld2View.as_view(),
        name='world2'),
]

urlpatterns = [url('^hello/', include(urls, namespace='hello'))]


