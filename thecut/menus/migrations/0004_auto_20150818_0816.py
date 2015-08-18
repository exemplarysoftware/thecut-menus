# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thecut.menus.validators


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_menuitem_site'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='viewlink',
            options={'ordering': ['name'], 'get_latest_by': 'publish_at', 'verbose_name': 'Internal link'},
        ),
        migrations.AlterModelOptions(
            name='weblink',
            options={'ordering': ['name'], 'get_latest_by': 'publish_at', 'verbose_name': 'External link'},
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='view',
            field=models.CharField(help_text='Django view URL name to resolve.', max_length=100, validators=[thecut.menus.validators.validate_view]),
        ),
    ]
