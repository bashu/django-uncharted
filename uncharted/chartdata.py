# -*- coding: utf-8 -*-

from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ForeignRelatedObjectsDescriptor


class DataProvider(object):

    def __init__(self, model=None, queryset=None, filters={}, fields=[],
                 related_fields={}, field_mappings=None, ordering=[]):

        if (model is None and queryset is None) or (model and queryset):
            raise AttributeError(
                "DataProvider class must be called with either Model class or QuerySet instance.")

        self.model, self.queryset = model, queryset
        self.filters = filters
        self.related_fields = related_fields
        self.ordering = ordering
        if field_mappings is None: field_mappings = []
        self.field_mappings = field_mappings
 
        self.fields = []
        self._values = {}

        model = queryset.model
        queryset = list(self.get_queryset())  # evaluating queryset

        for f in fields:
            try:
                if model._meta.get_field(f):
                    self._values[f] = [getattr(v, f) for v in queryset]
                    self.fields.append(f)
            except FieldDoesNotExist:
                try:
                    if isinstance(getattr(model, f), property):
                        self._values[f] = [getattr(v, f) for v in queryset]
                        self.fields.append(f)
                except AttributeError:
                    pass

                if isinstance(getattr(model, f), ForeignRelatedObjectsDescriptor):
                    for o in queryset:
                        related_fields = self.related_fields.get(f, {})

                        if related_fields.has_key('categoryField') and related_fields.has_key('valueField'):

                            for item in DataProvider(queryset=getattr(o, f).get_query_set(),
                                                     fields=related_fields.values()):

                                if self._values.has_key(item[related_fields['categoryField']]):
                                    self._values[item[related_fields['categoryField']]].append(
                                        item[related_fields['valueField']])
                                else:
                                    self._values[item[related_fields['categoryField']]] = list(
                                        item[related_fields['valueField']])

                                if not item[related_fields['categoryField']] in self.fields:
                                    self.fields.append(item[related_fields['categoryField']])

        self._results = []
        for f in self.fields:
            from_fields = [fm['fromField'] for fm in self.field_mappings]
            if f in from_fields:
                matches = [fm for fm in self.field_mappings if fm['fromField'] == f]
                for fm in matches:
                    field_name = fm['toField']
                    self._results.append(zip([
                        field_name for i in xrange(0, self.__len__())], self._values[f]))
            else:
                self._results.append(zip([f for i in xrange(0, self.__len__())], self._values[f]))

    def __len__(self):
        if not hasattr(self, '_count'):
            self._count = self.get_queryset().count()
        return self._count

    def __iter__(self):
        for r in zip(*self._results):
            yield dict((k, v) for k, v in r if v is not None)

    # def __getitem__(self, key):
    #     if not isinstance(key, int):
    #         raise TypeError, "DataProvider indices must be integers, not %s" % type(key)
    #     try:
    #         for f in self.fields:
    #             if f in [fm['fromField'] for fm in self.field_mappings]:
    #                 for fm in [fm for fm in self.field_mappings if fm['fromField'] == f]:
    #                     field_name = fm['toField']
    #                     if callable(field_name):
    #                         yield field_name(self._values, key)
    #                     else:
    #                         yield field_name, self._values[f][key]
    #             else:
    #                 yield f, self._values[f][key]
    #     except IndexError:
    #         raise IndexError, "DataProvider index out of range"

    def get_queryset(self):
        if hasattr(self, '_queryset'):
            return self._queryset

        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        else:
            queryset = self.model._default_manager.get_query_set()

        if self.filters:
            queryset = queryset.filter(**self.filters)
        self._queryset = queryset.order_by(*self.ordering)

        return self._queryset
