# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-20 16:31
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('appointment', '0025_auto_20171021_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Classroom'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='custom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='end',
            field=models.IntegerField(
                choices=[('8', 8), ('9', 9), ('10', 10), ('11', 11), ('12', 12), ('13', 13), ('14', 14), ('15', 15),
                         ('16', 16), ('17', 17), ('18', 18), ('19', 19), ('20', 20), ('21', 21), ('22', 22),
                         ('23', 23)]),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='start',
            field=models.IntegerField(
                choices=[('8', 8), ('9', 9), ('10', 10), ('11', 11), ('12', 12), ('13', 13), ('14', 14), ('15', 15),
                         ('16', 16), ('17', 17), ('18', 18), ('19', 19), ('20', 20), ('21', 21), ('22', 22),
                         ('23', 23)]),
        ),
    ]