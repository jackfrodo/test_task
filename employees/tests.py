from django.test import TestCase
from django.http import QueryDict
from employees.filters import EmployeeFilter, perform_alpha_groups
from employees.models import Employee


class GroupedTestCase(TestCase):
    def test_employees_alpha_groups(self):
        groups = (self.number_in_group)
        for g in groups:
            employees = Employee.objects.all().filter(index__in=','.join(g.chars).order_by('index')
            if employees:
                index = g.name.split('-')
                self.assertEquals(index[0], employees[0].surname[0].upper())
                self.assertEquals(index[1], employees[::-1][0].surname[0].upper())


class EmployeeTestCase(TestCase):
    def test_form(self):
        request_get = QueryDict('departament=1&is_worked=2')
        f = EmployeeFilter(request_get, queryset=Employee.objects.all().order_by('surname'))
        self.assertTrue(f.form.is_valid())
