# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from ..models import MenuItem, MenuItemContentType
from rest_framework import serializers


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.Field(source='pk')
    url = serializers.HyperlinkedIdentityField(
        view_name='admin:menus_menuitem_api:contenttype_detail',
        lookup_field='pk')
    verbose_name = serializers.SerializerMethodField('get_verbose_name')
    verbose_name_plural = serializers.SerializerMethodField(
        'get_verbose_name_plural')

    class Meta(object):
        fields = ['id',  'url', 'verbose_name', 'verbose_name_plural']
        model = MenuItemContentType

    def __init__(self, *args, **kwargs):
        return super(ContentTypeSerializer, self).__init__(*args, **kwargs)

    def get_verbose_name(self, content_type):
        return content_type.model_class()._meta.verbose_name.title()

    def get_verbose_name_plural(self, content_type):
        return content_type.model_class()._meta.verbose_name_plural.title()


class ContentTypeWithObjectsSerializer(ContentTypeSerializer):

    objects = serializers.SerializerMethodField('get_objects')

    class Meta(ContentTypeSerializer.Meta):
        fields = ContentTypeSerializer.Meta.fields + ['objects']

    def get_objects(self, content_type):
        queryset = content_type.model_class().objects.all()
        return GenericSerializer(queryset, content_type.model_class()).data


class GenericSerializer(serializers.ModelSerializer):

    id = serializers.Field(source='pk')
    name = serializers.Field(source='__str__')

    class Meta(object):
        fields = ['id', 'name']

    def __init__(self, queryset_or_instance, model, *args, **kwargs):
        self.Meta.model = model
        return super(GenericSerializer, self).__init__(queryset_or_instance,
                                                       *args, **kwargs)


class MenuItemSerializer(serializers.ModelSerializer):

    id = serializers.Field(source='pk')
    is_menu = serializers.SerializerMethodField('get_is_menu')
    content_object = serializers.SerializerMethodField('get_content_object')

    class Meta(object):
        fields = ['id', 'is_menu', 'name', 'parent', 'order', 'lft', 'rght',
                  'content_type', 'content_object', 'object_id']
        model = MenuItem

    def get_is_menu(self, menuitem):
        return menuitem.is_menu()

    def get_content_object(self, menuitem):
        if menuitem.content_object:
            serializer = GenericSerializer(menuitem.content_object,
                                           menuitem.content_object.__class__)
            return serializer.data
