# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-27 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0013_auto_20160426_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='units',
            field=models.CharField(max_length=20000),
        ),
    ]
