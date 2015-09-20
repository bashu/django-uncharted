# -*- coding: utf-8 -*-

from bisect import bisect
from itertools import izip

from django.utils.safestring import mark_safe

from .options import Options
from .exceptions import FieldError, ReadOnlyError
from .fields import *

__all__ = [
    'amValueAxis',
]


class amBase(type):

    def __new__(cls, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, amBase)]
        if not parents:
            return super(amBase, cls).__new__(cls, name, bases, attrs)

        new_class = super(amBase, cls).__new__(cls, name, bases, attrs)
        meta = getattr(new_class, 'Meta', None)
        new_class.add_to_class('_meta', Options(meta))

        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        field_names = set([f.name for f in new_class._meta.local_fields])
        for base in parents:
            if not hasattr(base, '_meta'):
                continue
            for field in base._meta.local_fields:
                if field.name in field_names:
                    raise FieldError(
                        'Local field %r in class %r clashes with field of similar name from base class %r' % (
                            field.name, name, base.__name__))
                new_class._meta.parents[base] = field
        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class amObject(object):
    __metaclass__ = amBase

    def __init__(self, *args, **kwargs):
        args_len = len(args)
        if args_len > len(self._meta.fields):
            raise IndexError("Number of args exceeds number of fields")

        fields_iter = iter(self._meta.fields)
        if not kwargs:
            for val, field in izip(args, fields_iter):
                setattr(self, field.attname, val)
        else:
            # slower, kwargs-ready version...
            for val, field in izip(args, fields_iter):
                setattr(self, field.attname, val)
                kwargs.pop(field.name, None)

        for field in fields_iter:
            if kwargs:
                if kwargs.has_key(field.attname) and field.readonly:
                    raise ReadOnlyError("'%s' is a read-only property of class %s" % (
                        field.name, self.__class__))

                try:
                    value = kwargs.pop(field.name)
                except KeyError:
                    value = field.get_default()
            else:
                value = field.get_default()
            try:
                setattr(self, field.attname, value)
            except ReadOnlyError:
                self.__dict__[field.attname] = field.get_default()

        if kwargs:
            for prop in kwargs.keys():
                try:
                    if isinstance(getattr(self.__class__, prop), property):
                        setattr(self, prop, kwargs.pop(prop))
                except AttributeError:
                    pass
            if kwargs:
                raise TypeError(
                    "'%s' is an invalid keyword argument for this function" % kwargs.keys()[0])

    def get_internal_type(self):
        raise NotImplementedError

    def render(self, name, attrs=None):
        output = []
        output.append("var %(name)s = new AmCharts.%(class)s();" % {
            'name': name, 'class': self.get_internal_type()})

        for field in iter(self._meta.fields):
            if not field.has_changed(field.get_default(), getattr(self, field.attname)):
                continue
            if field.render:
                output.append(field.render_field(name, getattr(self, field.attname)))
        return mark_safe(u'\n'.join(output))


class amAxisBase(amObject):

    autoGridCount = BooleanField(default=True)
    axisAlpha = DecimalField(default=1)
    axisColor = StringField(default="#000000")
    axisThickness = NumberField(default=1)
    color = StringField()
    dashLength = NumberField(default=0)
    fillAlpha = DecimalField(default=0)
    fillColor = StringField(default="#FFFFFF")
    fontSize = NumberField()
    gridAlpha = DecimalField(default=0.2)
    gridColor = StringField(default="#000000")
    gridCount = NumberField(default=5)
    gridThickness = NumberField(default=1)
    ignoreAxisWidth = BooleanField(default=False)
    inside = BooleanField(default=False)
    labelFrequency = NumberField(default=1)
    labelRotation = NumberField(default=0)
    labelsEnabled = BooleanField(default=False)
    offset = NumberField(default=0)
    position = StringField()
    showFirstLabel = BooleanField(default=True)
    showLastLabel = BooleanField(default=True)
    tickLength = NumberField(default=5)
    title = StringField()
    titleBold = BooleanField(default=True)
    titleColor = StringField()
    titleFontSize = NumberField()

    def addGuide(self, guide):
        """Adds guide to the axis"""
        raise NotImplementedError

    def removeGuide(self, index):
        """Removes guide from the axis"""
        raise NotImplementedError


class amValueAxis(amAxisBase):
    creation_counter = 0

    axisTitleOffset = NumberField(default=10)
    baseCoord = NumberField(null=True, readonly=True)
    baseValue = NumberField(default=0)
    duration = StringField()
    durationUnits = ObjectField(default={"DD": "d. ", "hh": ":", "mm" :":", "ss": ""})
    gridType = StringField(default="polygons")
    includeGuidesInMinMax = BooleanField(default=False)
    includeHidden = BooleanField(default=False)
    integersOnly = BooleanField(default=False)
    # TODO: labelFunction 
    logarithmic = BooleanField(default=False)
    max = DecimalField(null=True, readonly=True)
    maximum = DecimalField()
    min = DecimalField(null=True, readonly=True)
    minimum = DecimalField()
    minMaxMultiplier = DecimalField(default=1)
    precision = DecimalField()
    radarCategoriesEnabled = BooleanField(default=True)
    recalculateToPercents = BooleanField(default=False)
    reversed = BooleanField(default=False)
    stackType = StringField(default="none")
    step = NumberField(null=True, readonly=True)
    synchronizationMultiplier = DecimalField()
    totalText =	StringField()
    totalTextColor = StringField()
    unit = StringField()
    unitPosition = StringField(default="right")
    usePrefixes = BooleanField(default=False)
    useScientificNotation = BooleanField(default=False)
    
    def __init__(self, name='valueAxis', *args, **kwargs):
        super(amValueAxis, self).__init__(*args, **kwargs)
        self.name = name

        self.creation_counter = amValueAxis.creation_counter
        amValueAxis.creation_counter += 1

    def __cmp__(self, other):
        # this is needed because bisect does not take a comparison function.
        return cmp(self.creation_counter, other.creation_counter)

    def get_internal_type(self):
        return "ValueAxis"

    def synchronizeWithAxis(self, axis):
        """
        One value axis can be synchronized with another value axis. You
        should set synchronizationMultiplyer in order for this to work.

        """
        raise NotImplementedError

    def zoomToValues(self, startValue, endValue):
        """XY Chart only. Zooms-in the axis to the provided values."""
        raise NotImplementedError
