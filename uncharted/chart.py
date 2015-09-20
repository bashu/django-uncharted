# -*- coding: utf-8 -*-

from bisect import bisect
from itertools import izip

from django.utils.safestring import mark_safe

from .options import Options
from .exceptions import FieldError, ReadOnlyError
from .fields import *

__all__ = [
    'amValueAxis',
    'amCategoryAxis',
    'amBalloon',
    'amGraph',
    'amTrendLine',
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


class amCategoryAxis(amAxisBase):

    boldPeriodBeginning = BooleanField(default=True)
    # TODO: categoryFunction
    dateFormats = ArrayField(default=[
        {"period": 'fff', "format": 'JJ:NN:SS'},
        {"period": 'ss', "format": 'JJ:NN:SS'},
        {"period": 'mm', "format": 'JJ:NN'},
        {"period": 'hh', "format": 'JJ:NN'},
        {"period": 'DD', "format": 'MMM DD'},
        {"period": 'WW', "format": 'MMM DD'},
        {"period": 'MM', "format": 'MMM'},
        {"period": 'YYYY', "format":'YYYY'},
    ])
    equalSpacing = BooleanField(default=False)
    forceShowField = StringField()
    gridPosition = StringField(default="middle")
    # TODO: labelFunction
    markPeriodChange = BooleanField(default=True)
    minPeriod = StringField(default="DD")
    parseDates = BooleanField(default=False)
    startOnAxis = BooleanField(default=False)

    def get_internal_type(self):
        return "CategoryAxis"


class amBalloon(amObject):

    adjustBorderColor = BooleanField(default=False)
    borderAlpha = DecimalField(default=1)
    borderColor = StringField(default="#FFFFFF")
    borderThickness = NumberField(default=2)
    bulletSize = NumberField(default=8)
    color = StringField(default="#FFFFFF")
    cornerRadius = NumberField(default=6)
    fillAlpha = DecimalField(default=1)
    fillColor = StringField(default="#CC0000")
    fontSize = NumberField()
    horizontalPadding = NumberField(default=8)
    pointerWidth = NumberField(default=10)
    showBullet = BooleanField(default=False)
    textAlign = StringField(default="middle")
    textShadowColor = StringField(default="#000000")
    verticalPadding = NumberField(default=5)

    def get_internal_type(self):
        return "AmBalloon"


class amGraph(amObject):
    creation_counter = 0

    alphaField = StringField()
    balloonColor = StringField()
    balloonText = StringField(default="[[value]]")
    # TODO: baloonFunction
    behindColumns = BooleanField(default=False)
    bullet = StringField(default="none")
    bulletAlpha = DecimalField(default=1)
    bulletBorderAlpha = DecimalField(default=1)
    bulletBorderColor = StringField()
    bulletBorderThickness = NumberField(default=2)
    bulletColor = StringField()
    bulletField = StringField()
    bulletOffset = NumberField(default=0)
    bulletSize = NumberField(default=8)
    bulletSizeField = StringField()
    closeField = StringField()
    color = StringField()
    colorField = StringField()
    connect = BooleanField(default=True)
    cornerRadiusTop = NumberField(default=0)
    cursorBulletAlpha = DecimalField(default=1)
    customBullet = StringField()
    customBulletField = StringField()
    dashLength = NumberField(default=0)
    descriptionField = StringField()
    fillAlphas = DecimalField(default=0)
    fillColors = ArrayField(default=[])
    fillColorsField = StringField()
    # TODO: fillToGraph
    fontSize = NumberField()
    gradientOrientation = StringField(default="vertical")
    hidden = BooleanField(default=False)
    hideBulletsCount = NumberField(default=0)
    highField = StringField()
    includeInMinMax = BooleanField(default=True)
    labelColorField = StringField()
    labelPosition = StringField(default="top")
    labelText = StringField()
    legendAlpha = DecimalField()
    legendColor = StringField()
    legendValueText = StringField()
    lineAlpha = DecimalField(default=1)
    lineColor = StringField()
    lineColorField = StringField()
    lineThickness = NumberField(default=1)
    lowField = StringField()
    markerType = StringField()
    maxBulletSize = NumberField(default=50)
    minBulletSize = NumberField(default=0)
    negativeBase = NumberField(default=0)
    negativeFillAlphas = DecimalField()
    negativeFillColors = ArrayField(default=[])
    negativeLineColor = StringField()
    numberFormatter = ObjectField(null=True)
    openField = StringField()
    pointPosition = StringField(default="middle")
    showAllValueLabels = BooleanField(default=False)
    showBalloon = BooleanField(default=True)
    showBalloonAt = StringField(default="close")
    showHandOnHover = BooleanField(default=False)
    stackable = BooleanField(default=True)
    title = StringField()
    type = StringField(default="line")
    urlField = StringField()
    urlTarget = StringField()
    valueAxis = AttributeField(attribute='attname')
    valueField = StringField()
    visibleInLegend = BooleanField(default=True)
    # xAxis = AttributeField(attribute='attname')
    xField = StringField()
    # yAxis = AttributeField(attribute='attname')
    yField = StringField()

    def __init__(self, name='graph', unique=True, *args, **kwargs):
        super(amGraph, self).__init__(*args, **kwargs)
        self.name = name
        self.unique = unique

        self.creation_counter = amGraph.creation_counter
        amGraph.creation_counter += 1

    def __cmp__(self, other):
        return cmp(self.creation_counter, other.creation_counter)

    def get_internal_type(self):
        return 'AmGraph'


class amTrendLine(amObject):
    creation_counter = 0

    dashLength = NumberField(default=0)
    finalCategory = StringField()
    finalDate = DateField()
    finalValue = DecimalField()
    finalXValue = DecimalField()
    initialCategory = StringField()
    initialDate = DateField()
    initialValue = DecimalField()
    initialXValue = DecimalField()
    isProtected = BooleanField(default=False)
    lineAlpha = DecimalField(default=1)
    lineColor = StringField(default="#00CC00")
    lineThickness = NumberField(default=1)
    # valueAxis = AttributeField(attribute='attname')
    # valueAxisX = AttributeField(attribute='attname')

    def __init__(self, name='trendLine', *args, **kwargs):
        super(amTrendLine, self).__init__(*args, **kwargs)
        self.name = name

        self.creation_counter = amTrendLine.creation_counter
        amTrendLine.creation_counter += 1

    def __cmp__(self, other):
        return cmp(self.creation_counter, other.creation_counter)

    def get_internal_type(self):
        return 'TrendLine'
