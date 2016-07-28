# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from . import views

urls = [
    url(r'^world/$', views.HelloWorldView.as_view(), name='world'),
]

urlpatterns = [url('^hello/', include(urls, namespace='hello'))]

"""

urlpatterns = [
    # View Tester
    url(r'^hello/', include('test_app.hello.urls')),
]
"""

