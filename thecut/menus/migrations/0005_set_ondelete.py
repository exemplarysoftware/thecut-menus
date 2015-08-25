# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_auto_20150818_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='content_type',
            field=models.ForeignKey(related_name='+', blank=True, to='menus.MenuItemContentType', null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='publish_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='site',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sites.Site', null=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='publish_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='publish_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
