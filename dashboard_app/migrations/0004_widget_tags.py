# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-11 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0003_auto_20190911_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='dashboard_app.Tag'),
        ),
    ]
