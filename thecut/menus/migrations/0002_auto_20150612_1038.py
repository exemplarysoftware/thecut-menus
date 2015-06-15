# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='viewlink',
            options={'get_latest_by': 'publish_at', 'verbose_name': 'Internal link'},
        ),
        migrations.AlterModelOptions(
            name='weblink',
            options={'get_latest_by': 'publish_at', 'verbose_name': 'External link'},
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='name',
            field=models.CharField(help_text='Friendly display name.', max_length=100),
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='view',
            field=models.CharField(help_text='Django view URL name to resolve.', max_length=100),
        ),
    ]
