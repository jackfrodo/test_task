# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Departament(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, db_index=True)
    patronymic = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    start_working_date = models.DateField(db_index=True)
    end_working_date = models.DateField(null=True, db_index=True)
    position = models.CharField(max_length=200)
    departament = models.ForeignKey(Departament)
    index = models.CharField(max_length=1, db_index=True)

    def __unicode__(self):
        return "%s %s %s" % (self.surname, self.name, self.patronymic,)


@receiver(pre_save, sender=Employee)
def add_index(sender, instance, *args, **kwargs):
    instance.index = instance.surname[0].upper()
