# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 07:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20161013_1450'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([]),
        ),
    ]