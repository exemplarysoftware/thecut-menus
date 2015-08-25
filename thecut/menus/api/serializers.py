# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .. import settings
from ..models import MenuItem, MenuItemContentType
from rest_framework import serializers

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    # Django < 1.7 compatibility.
    from django.contrib.sites.models import get_current_site


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField(source='pk')

    verbose_name = serializers.SerializerMethodField()

    verbose_name_plural = serializers.SerializerMethodField()

    class Meta(object):
        extra_kwargs = {
            'url': {'view_name': 'admin:menus_menuitem_api:contenttype_detail'}
        }
        fields = ['url', 'id', 'verbose_name', 'verbose_name_plural']
        model = MenuItemContentType

    def get_verbose_name(self, content_type):
        return content_type.model_class()._meta.verbose_name.title()

    def get_verbose_name_plural(self, content_type):
        return content_type.model_class()._meta.verbose_name_plural.title()


class ContentTypeWithObjectsSerializer(ContentTypeSerializer):

    objects = serializers.SerializerMethodField()

    class Meta(ContentTypeSerializer.Meta):
        fields = ContentTypeSerializer.Meta.fields + ['objects']

    def get_objects(self, content_type):
        model = content_type.model_class()
        queryset = model.objects.all()
        if settings.SITE_FILTER and hasattr(model, 'site'):
            queryset = queryset.filter(
                site=get_current_site(self.context['request']))
        return GenericSerializer(queryset, many=True,
                                 model=content_type.model_class()).data


class GenericSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='pk')

    name = serializers.SerializerMethodField()

    class Meta(object):
        fields = ['id', 'name']

    def __init__(self, queryset, model, **kwargs):
        self.Meta.model = model
        return super(GenericSerializer, self).__init__(queryset, **kwargs)

    def get_name(self, instance):
        return instance.__str__().title()


class MenuItemSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='pk')

    content_object = serializers.SerializerMethodField()

    content_type_name = serializers.SerializerMethodField()

    class Meta(object):
        fields = ['id', 'is_menu', 'title', 'parent', 'order', 'lft', 'rght',
                  'content_type', 'content_object', 'object_id',
                  'content_type_name']
        model = MenuItem
        read_only_fields = ['order', 'lft', 'rght']

    def create(self, validated_data):
        ModelClass = self.Meta.model
        instance = ModelClass(**validated_data)
        instance.insert_at(instance.parent, position='last-child', save=True)
        return instance

    def get_content_object(self, menuitem):
        if menuitem.content_object:
            return GenericSerializer(
                menuitem.content_object,
                model=menuitem.content_object.__class__).data

    def get_content_type_name(self, menuitem):
        if menuitem.content_type:
            return menuitem.content_type.name.title()
