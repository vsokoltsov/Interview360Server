# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-30 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0007_auto_20180130_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='resume',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to='resumes.Resume'),
        ),
    ]
