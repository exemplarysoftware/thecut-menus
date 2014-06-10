# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework import authentication, generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .permissions import MenuItemAPIPermissions


class APIMixin(object):

    authentication_classes = [authentication.SessionAuthentication]
    paginate_by = 10
    paginate_by_param = 'limit'
    max_paginate_by = 100
    permission_classes = [permissions.IsAdminUser, MenuItemAPIPermissions]


class RootAPIView(APIMixin, APIView):

    # Can't use model-based permissions on the root API view.
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        return Response({
            'contentttypes':
            reverse('admin:menus_menuitem_api:contenttype_list',
                    request=request)
        })


class ContentTypeListAPIView(APIMixin, generics.ListAPIView):

    model = ContentType
    serializer_class = serializers.ContentTypeSerializer


class ContentTypeRetrieveAPIView(APIMixin, generics.RetrieveAPIView):

    model = ContentType
    serializer_class = serializers.ContentTypeWithObjectsSerializer
