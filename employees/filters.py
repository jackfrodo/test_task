# -*- coding: utf-8 -*-
from django_filters import FilterSet, MethodFilter, BooleanFilter
from employees.models import Employee
from django.db.models import Count
from employees.models import Employee


def in_company_filter(queryset, value):
    return queryset.filter(
            end_working_date__isnull=value
    )


class EmployeeFilter(FilterSet):
    in_company = BooleanFilter(action = in_company_filter)

    class Meta:
        model = Employee
        fields = ['departament']


class AlphaGroup(object):
    def __init__(self, chars, name):
        self.chars = list(chars)
        self.name = name


def perform_alpha_groups(max_alpha_groups):
    """Создает список по первым буквам фамили с объединенеим в группы (селекторы)

    максимально групп max_alpha_groups
    """
    alpha_groups = []

    rr = Employee.objects.all().values('index').annotate(count=Count('index')).order_by('index')
    count_elems = 0
    current_count = 0
    current_alpha = []
    if len(rr) > 0:
        count_elems = sum(item['count'] for item in rr)
        min_elems_in_group  = max(item['count'] for item in rr)
        count_in_group = count_elems / 7
        max_elems_in_group = max({count_in_group, min_elems_in_group})
        for item in rr:
            current_count += item['count']
            current_alpha.append(item['index'])
            if current_count >= max_elems_in_group:
                name = current_alpha[0] + " - " + current_alpha[-1]
                group = AlphaGroup(current_alpha, name)
                alpha_groups.append(group)
                current_count = 0
                current_alpha[:] = []

    if current_count > 0:
        name = current_alpha[0] + " - " + current_alpha[-1]
        group = AlphaGroup(current_alpha, name)
        alpha_groups.append(group)
        current_count = 0
        current_alpha[:] = []

    return alpha_groups
