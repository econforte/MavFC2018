# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcomputer', '0004_auto_20170206_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='model_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Model ID'),
        ),
        migrations.AddField(
            model_name='devicetype',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
