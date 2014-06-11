# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import forms
from . import serializers
from ..models import MenuItem, MenuItemContentType
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .permissions import MenuItemAPIPermissions


class APIMixin(object):

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser, MenuItemAPIPermissions]


class RootAPIView(APIMixin, APIView):

    # Can't use model-based permissions on the root API view.
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        return Response({
            # ContentType
            'contentttypes': reverse(
                'admin:menus_menuitem_api:contenttype_list', request=request),

            # MenuItem
            'menuitems': reverse(
                'admin:menus_menuitem_api:menuitem_list', request=request)
        })


class ContentTypeListAPIView(APIMixin, generics.ListAPIView):

    model = MenuItemContentType
    serializer_class = serializers.ContentTypeSerializer


class ContentTypeRetrieveAPIView(APIMixin, generics.RetrieveAPIView):

    model = MenuItemContentType
    serializer_class = serializers.ContentTypeWithObjectsSerializer


class MenuItemListAPIView(APIMixin, generics.ListAPIView):

    model = MenuItem
    serializer_class = serializers.MenuItemSerializer
    form_class = forms.MenuItemFilterForm

    def list(self, request, *args, **kwargs):
        root = request.QUERY_PARAMS.get('root')
        self.form = self.form_class(data={'root': root})
        if not self.form.is_valid():
            return Response(self.form.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return super(MenuItemListAPIView, self).list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super(MenuItemListAPIView, self).get_queryset(*args,
                                                                 **kwargs)
        return self.form.filter_queryset(queryset)
