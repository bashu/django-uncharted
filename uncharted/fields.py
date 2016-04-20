# -*- coding: utf-8 -*-

import re
import datetime
from decimal import Decimal

try:
    from django.utils import importlib
except ImportError:
    import importlib
from django.utils.safestring import mark_safe

from . import utils
from .exceptions import ReadOnlyError

ansi_date_re = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')

__all__ = [
    'StringField',
    'NumberField',
    'DecimalField',
    'DateField',
    'BooleanField',
    'ArrayField',
    'ObjectField',
    'AttributeField',
    'InstanceField',
]


class NOT_PROVIDED:
    pass


class FieldBase(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(FieldBase, cls).__new__(cls, name, bases, attrs)
        new_class.contribute_to_class = make_contrib(
            new_class, attrs.get('contribute_to_class'))
        return new_class


def make_contrib(superclass, func=None):
    class Creator(object):

        def __init__(self, field):
            self.field = field

        def __get__(self, obj, type=None):
            if obj is None:
                raise AttributeError('Can only be accessed via an instance.')
            return obj.__dict__[self.field.attname]

        def __set__(self, obj, value):
            if getattr(self.field, 'readonly', False):
                raise ReadOnlyError(
                    "'%s' is a read-only property of class %s" % (
                        self.field.name, obj.__class__),
                )
            obj.__dict__[self.field.attname] = self.field.to_python(value)

    def contribute_to_class(self, cls, name):
        if func:
            func(self, cls, name)
        else:
            super(superclass, self).contribute_to_class(cls, name)
        setattr(cls, self.name, Creator(self))

    return contribute_to_class


class Field(object):
    __metaclass__ = FieldBase

    empty_strings_allowed = True
    creation_counter = 0

    def __init__(self, name=None, default=NOT_PROVIDED, null=True, readonly=False, render=True):
        self.name = name
        self.default = default
        self.null = null
        self.readonly = readonly
        self.render = render

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __cmp__(self, other):
        # this is needed because bisect does not take a comparison function.
        return cmp(self.creation_counter, other.creation_counter)

    def has_default(self):
        """Returns a boolean of whether this field has a default value."""
        return self.default is not NOT_PROVIDED

    def get_default(self):
        """Returns the default value for the field."""
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        if not self.empty_strings_allowed or self.null:
            return None
        return ""

    def contribute_to_class(self, cls, name):
        self.name = self.attname = name
        self.chart = cls
        cls._meta.add_field(self)

    def prepare_value(self, value):
        return utils.dumps(value)

    def to_python(self, value):
        return value

    def has_changed(self, initial, value):
        if initial != value:
            return True
        return False

    def render_field(self, name, value, attrs=None):
        if value is None:
            value = ''

        return mark_safe(u"%(name)s.%(attname)s = %(value)s;" % {
            'name': name,
            'attname': self.attname,
            'value': self.prepare_value(value),
        })


class StringField(Field):

    def to_python(self, value):
        if value is None:
            return None
        return unicode(value)


class NumberField(Field):
    empty_strings_allowed = False

    def to_python(self, value):
        if value is None:
            return None
        return int(value)


class DecimalField(Field):
    empty_strings_allowed = False

    def prepare_value(self, value):
        return utils.dumps(round(float(value), 2))

    def to_python(self, value):
        if value is None:
            return None
        return Decimal(repr(value))


class DateField(Field):
    empty_strings_allowed = False

    def prepare_value(self, value):
        value = datetime.datetime(value.year, value.month, value.day, 12)
        return super(DateField, self).prepare_value(value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value

        if ansi_date_re.search(value):
            # Now that we have the date string in YYYY-MM-DD format,
            # check to make sure it's a valid date.  We could use
            # time.strptime here and catch errors, but datetime.date
            # produces much friendlier error messages.
            year, month, day = map(int, value.split('-'))
            try:
                return datetime.date(year, month, day)
            except ValueError:
                return None


class BooleanField(Field):
    empty_strings_allowed = False

    def to_python(self, value):
        if value is None:
            return None
        return bool(value)


class ArrayField(Field):

    def to_python(self, value):
        if value is None:
            return None
        return list(value)


class ObjectField(Field):

    def render_field(self, name, value, attrs=None):
        if value is None:
            value = {}

        output = []
        output.append("%(name)s.%(attname)s = new Object();" % {
            'name': name, 'attname': self.attname})

        for k, v in value.items():
            output.append(u"%(name)s.%(attname)s.%(property)s = %(value)s;" % {
                'name': name,
                'attname': self.attname,
                'property': k,
                'value': self.prepare_value(v),
            })
        return mark_safe(u'\n'.join(output))

    def to_python(self, value):
        if value is None:
            return None
        return dict(value)


class AttributeField(Field):

    def __init__(self, name=None, attribute='attrname', *args, **kwargs):
        super(AttributeField, self).__init__(name, *args, **kwargs)
        self.attribute = attribute

    def prepare_value(self, value):
        return getattr(value, self.attribute)

    def has_changed(self, initial, value):
        if getattr(initial, self.attribute, None) != getattr(value, self.attribute, None):
            return True
        return False


class InstanceField(Field):
    empty_strings_allowed = False
    is_related = True

    def __init__(self, klass, *args, **kwargs):
        super(InstanceField, self).__init__(*args, **kwargs)
        self._klass = klass

    def get_default(self):
        if self.null and not self.readonly:
            return None
        return self.klass()

    @property
    def klass(self):
        if not isinstance(self._klass, basestring):
            return self._klass

        # it's a string, let's figure it out.
        if '.' in self._klass:
            module_bits = self._klass.split('.')
            module_path, class_name = '.'.join(
                module_bits[:-1]), module_bits[-1]
            module = importlib.import_module(module_path)
        else:
            raise ImportError("Uncharted requires a Python-style path (<module.Class>) to lazy load related resources. Only given '%s'." % self._klass)

        klass = getattr(module, class_name, None)

        if klass is None:
            raise ImportError(
                "Module '%s' does not appear to have a class called '%s'." % (
                    module_path, class_name),
            )

        return klass

    def render_field(self, name, value, attrs=None):
        if value is None:
            value = ''

        output = []
        if self.readonly is True:
            output.append(
                "var %(attname)s = %(name)s.%(attname)s;" % {
                    'name': name, 'attname': self.attname})

        else:
            output.append(
                "var %(attname)s = new AmCharts.%(class)s();" % {
                    'name': name,
                    'attname': self.attname,
                    'class': value.get_internal_type(),
                })

        for f in iter(value._meta.fields):
            if not f.has_changed(f.get_default(), getattr(value, f.attname)):
                continue
            output.append(
                f.render_field(self.attname, getattr(value, f.attname)))

        return mark_safe(u'\n'.join(output))
