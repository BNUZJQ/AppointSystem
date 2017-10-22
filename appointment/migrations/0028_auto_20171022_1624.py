# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-22 08:24
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('appointment', '0027_auto_20171021_0044'),
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
                choices=[(8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17),
                         (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)]),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='start',
            field=models.IntegerField(
                choices=[(8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17),
                         (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)]),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.IntegerField(
                choices=[(0, b'\xe6\x9c\xaa\xe5\x88\xb0\xe9\xa2\x84\xe7\xba\xa6\xe6\x97\xb6\xe9\x97\xb4'),
                         (1, b'\xe6\x9f\x9c\xe9\x97\xa8\xe5\xb7\xb2\xe6\x89\x93\xe5\xbc\x80'),
                         (2, b'\xe5\xb7\xb2\xe5\x8f\x96\xe8\xb5\xb0\xe9\x92\xa5\xe5\x8c\x99'),
                         (3, b'\xe9\x92\xa5\xe5\x8c\x99\xe5\xb7\xb2\xe8\xbf\x98'),
                         (4, b'\xe9\xa2\x84\xe7\xba\xa6\xe5\xb7\xb2\xe5\x8f\x96\xe6\xb6\x88')], default=0),
        ),
    ]