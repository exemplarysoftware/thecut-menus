# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('menus', '0002_auto_20150612_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, blank=True, to='sites.Site', null=True),
        ),
    ]
