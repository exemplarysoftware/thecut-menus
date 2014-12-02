# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_enabled', models.BooleanField(default=True, db_index=True, verbose_name='enabled')),
                ('is_featured', models.BooleanField(default=False, db_index=True, verbose_name='featured')),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now, help_text='This item will only be viewable on the website if it is enabled, and this date and time has past.', verbose_name='publish date & time', db_index=True)),
                ('expire_at', models.DateTimeField(help_text='This item will no longer be viewable on the website if this date and time has past. Leave blank if you do not wish this item to expire.', null=True, verbose_name='expiry date & time', db_index=True, blank=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('image', models.ImageField(upload_to='uploads/menus', blank=True)),
                ('slug', models.SlugField(unique=True, null=True)),
                ('object_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('created_by', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='menus.MenuItem', null=True)),
                ('publish_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'publish_at',
                'verbose_name': 'menu',
                'verbose_name_plural': 'menus',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ViewLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_enabled', models.BooleanField(default=True, db_index=True, verbose_name='enabled')),
                ('is_featured', models.BooleanField(default=False, db_index=True, verbose_name='featured')),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now, help_text='This item will only be viewable on the website if it is enabled, and this date and time has past.', verbose_name='publish date & time', db_index=True)),
                ('expire_at', models.DateTimeField(help_text='This item will no longer be viewable on the website if this date and time has past. Leave blank if you do not wish this item to expire.', null=True, verbose_name='expiry date & time', db_index=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('view', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL)),
                ('publish_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'publish_at',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_enabled', models.BooleanField(default=True, db_index=True, verbose_name='enabled')),
                ('is_featured', models.BooleanField(default=False, db_index=True, verbose_name='featured')),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now, help_text='This item will only be viewable on the website if it is enabled, and this date and time has past.', verbose_name='publish date & time', db_index=True)),
                ('expire_at', models.DateTimeField(help_text='This item will no longer be viewable on the website if this date and time has past. Leave blank if you do not wish this item to expire.', null=True, verbose_name='expiry date & time', db_index=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('created_by', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL)),
                ('publish_by', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='+', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'publish_at',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItemContentType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contenttypes.contenttype',),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='content_type',
            field=models.ForeignKey(blank=True, to='menus.MenuItemContentType', null=True),
            preserve_default=True,
        ),
    ]
