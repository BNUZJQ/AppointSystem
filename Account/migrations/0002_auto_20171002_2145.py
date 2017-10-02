# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-02 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.IntegerField(choices=[(0, 'Student'), (1, 'Teacher'), (2, 'Admin')], default=0, max_length=10),
        ),
    ]