# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import thecut.menus.validators


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_set_ondelete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewlink',
            name='view',
            field=models.CharField(help_text='Django view URL name to resolve. Format view:link arg1 arg2', max_length=100, validators=[thecut.menus.validators.validate_view]),
        ),
    ]
