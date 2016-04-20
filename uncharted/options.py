# -*- coding: utf-8 -*-

from bisect import bisect

try:
    from django.utils.datastructures import SortedDict
except ImportError:
    from collections import OrderedDict as SortedDict

from .exceptions import FieldDoesNotExist


class Options(object):

    def __init__(self, meta):
        self.local_fields = []
        self.parents = SortedDict()
        self.object_name = None

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.object_name = cls.__name__

    def add_field(self, field):
        self.local_fields.insert(bisect(self.local_fields, field), field)

    @property
    def fields(self):
        fields = []
        for parent in self.parents:
            fields.extend(parent._meta.fields)
        fields.extend(self.local_fields)
        return fields

    def get_field(self, name):
        for f in self.fields:
            if f.name == name:
                return f
        raise FieldDoesNotExist(
            '%s has no field named %r' % (self.object_name, name))
