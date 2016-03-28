# -*- coding: utf-8 -*-
from django_filters import FilterSet, MethodFilter, BooleanFilter
from employees.models import Employee
from django.db.models import Count
from django.db.models.functions import Substr,Upper

def in_company_filter(queryset, value):
    return queryset.filter(
            end_working_date__isnull=value
    )


class EmployeeFilter(FilterSet):
    in_company = BooleanFilter(action = in_company_filter)

    class Meta:
        model = Employee
        fields = ['departament']

class AlphaItem(object):
    """Элемент селектора

    Объект единичного элемента селектора
    предоставляет ряд методом и свойств
    """
    def __init__(self, letter, count_items):
        self.letters = list(letter)
        self.count_items = count_items
        self.flush = False

    def get_name(self):
        return self.letters[0] + " - " + self.letters[-1]

    def get_chars(self):
        return ", ".join(self.letters)

    def add_letter(self, letter, count_items, append_after = True):
        if append_after:
            self.letters.extend(list(letter))
        else:
            tmp = list(letter)
            tmp.extend(self.letters)
            self.letters = list(tmp)
        self.count_items += count_items

class AlphaGroup(object):
    """Cелектор

    Объект единичного элемента селектора
    предоставляет ряд методом и свойств
    """
    def __init__(self, max_groups):
        self.max_groups = max_groups
        self.items = []
        self.current_count = 0
        self.max_in_group = 0
        self.normalize = 0


    def add(self, letter, count_items):
        item = AlphaItem(letter, count_items)
        self.items.append(item)


    def preform_union(self):
        """Объединнение в группы

        Идем по списку через enumerate. передвигая индекс элемента, в который объединяем
        """
        if not self.items:
            return
        if len(self.items) == 1:
            return
        cur_index = 0
        for index, item in enumerate(self.items):
            if cur_index == index:
                continue
            if self.items[cur_index].count_items >= self.max_in_group:
                cur_index = index
                continue
            if item.count_items >= self.max_in_group:
                cur_index = index
                continue
            else:
                self.items[cur_index].add_letter(item.letters, item.count_items)
                item.flush = True
        self.flush()


    def flush(self):
        """Очищаем список от ненужных

        Идем по списку через enumerate. Отбираем элементы без объединения
        """
        tmp = []
        for index, item in enumerate(self.items):
            if not item.flush:
                tmp.append(item)
        self.items = list(tmp)


    def preform_normalize(self):
        """Приводим списко к однообразию по количеству элементов

        Идем по списку через enumerate. Отбираем элементы, где количество менее половины.
        Ищем близлижайщие с меньшим количеством и добавлем туда
        """
        if not self.items:
            return
        if len(self.items) == 1:
            return
        for index, item in enumerate(self.items):
            if not item.flush and item.count_items <= self.normalize:
                prev_item = None
                next_item = None
                appenf_after = False
                try:
                    prev_item = self.items[index - 1]
                except:
                    pass
                try:
                    next_item = self.items[index + 1]
                except:
                    pass
                union_item = next_item
                if prev_item and next_item:
                    union_item = prev_item
                    if next_item.count_items < prev_item.count_items:
                        union_item = next_item
                    else:
                        appenf_after = True
                elif prev_item:
                    appenf_after = True
                    union_item = prev_item
                union_item.add_letter(item.letters, item.count_items, appenf_after)
                item.flush = True
        self.flush()


    def perform(self):
        """Создает список по первой букве фамилии

        Делаем запрос к модели и выбираем буква + количество
        вызываем методы
        """

        rr = Employee.objects.annotate(sletter=Substr(Upper('surname'),1,1)).values('sletter').annotate(count=Count('sletter')).order_by('sletter').all()

        if len(rr) > 0:
            count_elems = sum(item['count'] for item in rr)
            min_elems_in_group  = max(item['count'] for item in rr)
            count_in_group = count_elems / self.max_groups
            self.max_in_group = max({count_in_group, min_elems_in_group})
            self.normalize = self.max_in_group / 2
            for item in rr:
                self.add(item['sletter'], item['count'])

            self.preform_union()
            self.preform_normalize()

