# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-24 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0003_remove_trips_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trips',
            name='start',
            field=models.DateField(),
        ),
    ]
