# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-03 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_auto_20171002_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.IntegerField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')],
                                      default=0),
        ),
    ]