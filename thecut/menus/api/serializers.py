# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes.models import ContentType
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
        model = ContentType

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
        return GenericSerializer(queryset).data


class GenericSerializer(serializers.ModelSerializer):

    id = serializers.Field(source='pk')
    name = serializers.Field(source='__str__')

    class Meta(object):
        fields = ['id', 'name']

    def __init__(self, instance, *args, **kwargs):
        self.Meta.model = instance.model
        return super(GenericSerializer, self).__init__(instance, *args,
                                                       **kwargs)
