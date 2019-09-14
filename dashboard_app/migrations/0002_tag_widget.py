# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-11 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('title_info', models.TextField()),
                ('baseline_value', models.IntegerField(blank=True, help_text='Filled automatically from data_points.', null=True)),
                ('baseline_info', models.TextField(blank=True)),
                ('best_goal', models.IntegerField(choices=[(1, 'Higher'), (-1, 'Lower')], help_text="Required. Note, sometimes the 'best' number will be the lowest one (example: tracking Missing Books).")),
                ('best_value', models.IntegerField(blank=True, help_text='Filled automatically from data_points.', null=True)),
                ('best_value_info', models.TextField(blank=True)),
                ('current_value', models.IntegerField(blank=True, help_text='Filled automatically from data_points.', null=True)),
                ('current_value_info', models.TextField(blank=True)),
                ('trend_direction', models.IntegerField(blank=True, choices=[(1, 'Up'), (-1, 'Down'), (0, 'Flat')], help_text='Filled automatically from data_points.', null=True)),
                ('trend_color', models.IntegerField(blank=True, choices=[(1, 'Good'), (-1, 'Bad'), (0, 'Not Applicable')], help_text="Filled automatically from data_points and 'best goal'.", null=True)),
                ('trend_info', models.TextField(blank=True)),
                ('data_points', models.TextField(help_text='Data may be filled programatically. If entered manually, it should consist of valid json, formatted like this: [ {"March_2008": 123}, {"April_2008": 456} ]')),
                ('max_data_points_count', models.IntegerField(blank=True, help_text='Optional. Maximum number of data_points; i.e. 12 for a yearly month-by-month widget.', null=True)),
                ('key_label', models.CharField(help_text="A brief description of the 'key' in the above 'data points' key-value pairs.", max_length=50)),
                ('value_label', models.CharField(help_text="A brief description of the 'value' in the above 'data points' key-value pairs.", max_length=50)),
                ('data_contact_name', models.CharField(max_length=50)),
                ('data_contact_email_address', models.EmailField(max_length=254)),
                ('more_info_url', models.URLField(blank=True, help_text='Not required, but strongly suggested.')),
                ('active', models.BooleanField(default=True, help_text='Means data is still being collected for this widget.')),
            ],
        ),
    ]