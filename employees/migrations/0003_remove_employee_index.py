# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 10:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20160325_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='index',
        ),
    ]