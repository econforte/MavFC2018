# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcomputer', '0013_auto_20170325_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='unittype',
            name='max_limit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='unittype',
            name='min_limit',
            field=models.FloatField(blank=True, null=True),
        ),
    ]