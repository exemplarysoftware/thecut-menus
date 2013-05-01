# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse


class HttpResponseCreated(HttpResponse):
    status_code = 201
