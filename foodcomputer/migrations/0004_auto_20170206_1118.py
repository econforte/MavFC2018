# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcomputer', '0003_auto_20170206_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatype',
            name='max_limit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datatype',
            name='min_limit',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
