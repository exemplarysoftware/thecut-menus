# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import forms, permissions, serializers
from ..models import MenuItem, MenuItemContentType
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import generic
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import authentication, generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIMixin(object):

    authentication_classes = [authentication.SessionAuthentication]

    permission_classes = [permissions.IsAdminUser,
                          permissions.MenuItemPermissions]

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(APIMixin, self).dispatch(*args, **kwargs)


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


class MenuItemRetrieveAPIView(APIMixin, generics.RetrieveUpdateDestroyAPIView):

    model = MenuItem
    serializer_class = serializers.MenuItemSerializer


class MenuItemCreateAPIView(APIMixin, generics.CreateAPIView):

    model = MenuItem
    serializer_class = serializers.MenuItemSerializer

    def create(self, request, *args, **kwargs):
        # The `create` method of the CreateModelMixin is not very extensible,
        # so we're going to have blast over the entire method here.
        serializer = self.get_serializer(data=request.DATA,
                                         files=request.FILES)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        menuitem = serializer.object
        menuitem.created_by = menuitem.updated_by = request.user
        menuitem.insert_at(menuitem.parent, position='last-child', save=True)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class MenuItemMoveAPIView(generic.list.MultipleObjectMixin, generic.View):
    """Move a MenuItem to a different position in the tree."""

    model = MenuItem

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('menus.change_menuitem'):
            return HttpResponseForbidden(content_type='text/plain')

        return super(MenuItemMoveAPIView, self).dispatch(request, *args,
                                                         **kwargs)

    def post(self, *args, **kwargs):
        root_pk = self.kwargs.get('target_pk')
        root = get_object_or_404(MenuItem, pk=root_pk)

        ordered_pks = self.request.POST.getlist('pk')
        for pk in ordered_pks:
            item = get_object_or_404(MenuItem, pk=pk)
            item.move_to(root, 'last-child')
            item.save()

        return HttpResponse(content_type='text/plain')
