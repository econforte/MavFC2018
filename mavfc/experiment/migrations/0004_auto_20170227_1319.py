# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0003_remove_experimentrule_baseline_variance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentrule',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_rules', to='foodcomputer.Device'),
        ),
    ]
