# -*- coding: utf-8 -*-
from django_filters.views import FilterView
from django.views.generic import ListView
from employees.filters import EmployeeFilter, AlphaGroup
from django.db.models import Count
from employees.models import Employee
from django.db.models.functions import Substr,Upper

class EmployeeList(ListView):
    """Список сотрудников компании + форма фильтрации

    Применяется фильтр по данным из запроса
    Вывод постраничный
    """

    context_object_name = 'employees'
    template_name = 'employees/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        context['filter'] = self.filter_data
        context['departament'] = self.request.GET.get('departament', '')
        context['in_company'] = self.request.GET.get('in_company', 0)
        return context

    def get_queryset(self):
        offset, limit = self.request.GET.get('offset', 0), self.request.GET.get('limit', 0)
        self.filter_data = EmployeeFilter(self.request.GET, queryset=Employee.objects.all().order_by('surname'))
        employees = self.filter_data
        return employees


class RangeList(ListView):
    """Список по алфавитному указателю с выводом 7 селекторов (диапозонов)

    Применяется фильтр по данным из запроса
    Вывод постраничный
    """

    template_name = 'employees/range.html'
    context_object_name = 'employees'
    number_groups = 7
    alpha_groups = []

    def get_context_data(self, **kwargs):
        max_alpha_groups = 7
        context = super(RangeList, self).get_context_data(**kwargs)
        alpha_groups = AlphaGroup(max_alpha_groups)
        alpha_groups.perform()
        context['al_groups'] =  alpha_groups.items
        return context

    def get_queryset(self):
        alpha = self.request.GET.get('alpha', [])
        employees = []
        try:
            employees = Employee.objects.annotate(slatter=Substr(Upper('surname'),1,1)).filter(slatter__in=alpha)
        except ValueError:
            pass
        return employees
