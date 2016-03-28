# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter(name='addbs')
def addbs(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='joinby')
def joinby(value, arg):
    return arg.join(value)
