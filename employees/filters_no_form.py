# -*- coding: utf-8 -*-
from django_filters import FilterSet,MethodFilter
from employees.models import Employee


class EmployeeFilter(FilterSet):
    in_company = MethodFilter()

    class Meta:
        model = Employee
        fields = ['departament']

    def filter_in_company(self, queryset, value):
        return queryset.filter(
            end_working_date__isnull=value
        )

