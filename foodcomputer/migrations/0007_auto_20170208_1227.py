# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 18:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcomputer', '0006_auto_20170206_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='lower_variance',
            new_name='lower_threshold',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='upper_variance',
            new_name='upper_threshold',
        ),
    ]
