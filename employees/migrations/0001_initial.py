# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 16:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(db_index=True, max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('start_working_date', models.DateField(db_index=True)),
                ('end_working_date', models.DateField(db_index=True, null=True)),
                ('position', models.CharField(max_length=200)),
                ('index', models.CharField(db_index=True, max_length=1)),
                ('departament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Departament')),
            ],
        ),
    ]
