# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-29 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='veg_type',
            field=models.CharField(choices=[('n', '普通'), ('w', '水菜')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
