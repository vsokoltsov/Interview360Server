# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-04 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='specialties',
            field=models.ManyToManyField(to='companies.Specialty'),
        ),
    ]
