# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 00:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcomputer', '0008_auto_20170208_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='name',
        ),
    ]
