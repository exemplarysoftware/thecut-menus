# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic import View
from django.http import HttpResponse

class HelloWorldView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Hello World")



