# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-21 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20170819_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymember',
            name='active',
            field=models.BooleanField(default=True),
        )
    ]
