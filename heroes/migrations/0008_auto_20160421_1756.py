# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-21 17:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0007_battle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='battle',
            old_name='all_units_stats',
            new_name='units',
        ),
    ]
