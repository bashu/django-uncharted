# -*- coding: utf-8 -*-

import copy
from bisect import bisect
from itertools import izip

from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict

from .options import Options
from .exceptions import FieldError, ReadOnlyError
from .fields import *

__all__ = [
    'amValueAxis',
    'amCategoryAxis',
    'amBalloon',
    'amGraph',
    'amTrendLine',
    'amChartCursor',
    'amChartScrollbar',
    'amRadarChart',
    'amSerialChart',
    'amXYChart',
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
    baseCoord = NumberField(null=True, readonly=True, render=False)
    baseValue = NumberField(default=0)
    duration = StringField()
    durationUnits = ObjectField(default={"DD": "d. ", "hh": ":", "mm" :":", "ss": ""})
    gridType = StringField(default="polygons")
    includeGuidesInMinMax = BooleanField(default=False)
    includeHidden = BooleanField(default=False)
    integersOnly = BooleanField(default=False)
    # TODO: labelFunction 
    logarithmic = BooleanField(default=False)
    max = DecimalField(null=True, readonly=True, render=False)
    maximum = DecimalField()
    min = DecimalField(null=True, readonly=True, render=False)
    minimum = DecimalField()
    minMaxMultiplier = DecimalField(default=1)
    precision = DecimalField()
    radarCategoriesEnabled = BooleanField(default=True)
    recalculateToPercents = BooleanField(default=False)
    reversed = BooleanField(default=False)
    stackType = StringField(default="none")
    step = NumberField(null=True, readonly=True, render=False)
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


class amChartCursor(amObject):

    bulletsEnabled = BooleanField(default=False)
    bulletSize = NumberField(default=8)
    categoryBalloonAlpha = DecimalField(default=1)
    categoryBalloonColor = StringField()
    categoryBalloonDateFormat = StringField(default="MMM DD, YYYY")
    categoryBalloonEnabled = BooleanField(default=True)
    color = StringField(default="#FFFFFF")
    cursorAlpha = DecimalField(default=1)
    cursorColor = StringField(default="#CC0000")
    cursorPosition = StringField()
    enabled = BooleanField(default=True)
    oneBalloonOnly = BooleanField(default=False)
    pan = BooleanField(default=False)
    selectionAlpha = DecimalField(default=1)
    selectWithoutZooming = BooleanField(default=False)
    valueBalloonsEnabled = BooleanField(default=True)
    zoomable = BooleanField(default=True)

    def get_internal_type(self):
        return "ChartCursor"

    def addListener(self, type, handler):
        """Adds event listener to the object."""
        raise NotImplementedError

    def removeListener(self):
        """Removes event listener from object."""
        raise NotImplementedError
    

class amChartScrollbar(amObject):

    autoGridCount = BooleanField(default=False)
    backgroundAlpha = DecimalField(default=1)
    backgroundColor = StringField(default="#D4D4D4")
    color = StringField()
    dragIconHeight = NumberField(default=18)
    dragIconWidth = NumberField(default=11)
    graph = AttributeField(attribute='attname')
    graphFillAlpha = DecimalField(default=0.1)
    graphFillColor = StringField(default="#000000")
    graphLineAlpha = DecimalField(default=0)
    graphLineColor = StringField(default="#000000")
    graphType = StringField()
    gridAlpha = DecimalField(default=0.7)
    gridColor = StringField(default="#FFFFFF")
    gridCount = NumberField(default=0)
    hideResizeGrips = BooleanField(default=False)
    maximum = DecimalField()
    minimum = DecimalField()
    resizeEnabled = BooleanField(default=True)
    scrollbarHeight = NumberField(default=20)
    scrollDuration = NumberField(default=2)
    selectedBackgroundAlpha = DecimalField(default=1)
    selectedBackgroundColor = StringField(default="#EFEFEF")
    selectedGraphFillAlpha = DecimalField(default=0.5)
    selectedGraphFillColor = StringField(default="#000000")
    selectedGraphLineAlpha = DecimalField(default=0)
    selectedGraphLineColor = StringField(default="#000000")
    updateOnReleaseOnly = BooleanField(default=False)
    
    def get_internal_type(self):
        return "ChartScrollbar"


class amChart(amObject):

    backgroundColor = StringField(default="#FFFFFF")
    balloon = InstanceField(klass=amBalloon, null=False, readonly=True)
    borderAlpha = DecimalField(default=0)
    borderColor = StringField(default="#000000")
    color = StringField(default="#000000")
    dataProvider = ArrayField()
    fontFamily = StringField(default="Verdana")
    fontSize = NumberField(default=11)
    height = StringField(default="100%")
    # TODO: legendDiv
    numberFormatter = ObjectField(default={
        "precision": -1,
        "decimalSeparator": '.',
        "thousandsSeparator": ',',
    })
    panEventsEnabled = BooleanField(default=False)
    pathToImages = StringField()
    percentFormatter = ObjectField(default={
        "precision": 2,
        "decimalSeparator": '.',
        "thousandsSeparator": ',',
    })
    prefixesOfBigNumbers = ArrayField(default=[
            {"number": 1e+3, "prefix": "k"},
            {"number": 1e+6, "prefix": "M"},
            {"number": 1e+9, "prefix": "G"},
            {"number": 1e+12, "prefix": "T"},
            {"number": 1e+15, "prefix": "P"},
            {"number": 1e+18, "prefix": "E"},
            {"number": 1e+21, "prefix": "Z"},
            {"number": 1e+24, "prefix": "Y"}])
    prefixesOfSmallNumbers = ArrayField(default=[
            {"number": 1e-24, "prefix": "y"},
            {"number": 1e-21, "prefix": "z"},
            {"number": 1e-18, "prefix": "a"},
            {"number": 1e-15, "prefix": "f"},
            {"number": 1e-12, "prefix": "p"},
            {"number": 1e-9, "prefix": "n"},
            {"number": 1e-6, "prefix": "μ"},
            {"number": 1e-3, "prefix": "m"}])
    usePrefixes = BooleanField(default=False)
    version = StringField(readonly=True, render=False)

    def __init__(self, name='chart', *args, **kwargs):
        super(amChart, self).__init__(*args, **kwargs)
        self.name = name
        self.listeners = SortedDict()
        self.trendLines = []

    def addLabel(self, *args, **kwargs):
        """
        Adds a label on a chart. You can use it for labeling axes, adding
        chart title, etc. x and y coordinates can be set in number,
        percent, or a number with ! in front of it - coordinate will
        be calculated from right or bottom instead of left or top.

        """
        raise NotImplementedError

    def clearLabels(self):
        """Removes all labels added to the chart."""
        raise NotImplementedError

    def addTitle(self, *args, **kwargs):
        """
        Adds title to the top of the chart. Pie, Radar positions are updated
        so that they won't overlap. Plot area of Serial/XY chart is also
        updated unless autoMargins property is set to false. You can add any
        number of titles - each of them will be placed in a new line. To
        remove titles, simply clear titles array: chart.titles = []; and call
        chart.validateNow() method.

        """
        raise NotImplementedError

    def addLegend(self, legend):
        """
        Adds a legend to the chart. By default, you don't need to create
        div for your legend, however if you want it to be positioned
        in some different way, you can create div anywhere you want
        and pass id or reference to your div as a second
        parameter.

        """
        raise NotImplementedError

    def removeLegend(self):
        """Removes chart's legend."""
        raise NotImplementedError

    def addListener(self, type, handler):
        """Adds event listener to the object."""
        try:
            self.listeners[type].append(copy.deepcopy(handler))
        except KeyError:
            self.listeners[type] = [(copy.deepcopy(handler))]

    def removeListener(self):
        """Removes event listener from chart object."""
        raise NotImplementedError

    def addTrendLine(self, trendline):
        """
        Adds a TrendLine to a chart. You should call chart.validateNow()
        after this method is called in order the trend line to be
        visible.

        """
        trendline.attname = trendline.name + str(trendline.creation_counter)
        self.trendLines.insert(bisect(self.trendLines, trendline), copy.deepcopy(trendline))

    def removeTrendLine(self, index):
        """
        Removes a trend line from a chart. You should call
        chart.validateNow() in order the changes to be visible.

        """
        raise NotImplementedError

    def render(self, name, attrs=None):
        output = [super(amChart, self).render(name, attrs)]

        # $(%(name)s).trigger('%(handler)s', [event]);
        for t, handlers in self.listeners.items():
            for h in handlers:
                output.append(
                    "%(name)s.addListener('%(type)s', function(event) {%(handler)s(event, %(name)s);})" % {
                        'name': name,
                        'type': t,
                        'handler': h,
                    })

        for trendline in self.trendLines:
            output.append(trendline.render(name=trendline.attname))
            output.append("%(name)s.addTrendLine(%(trendline)s);" % {
                'name': name, 'trendline': trendline.attname})

        return mark_safe(u'\n'.join(output))


class amCoordinateChart(amChart):

    colors = ArrayField(default=[
        "#FF6600",
        "#FCD202",
        "#B0DE09",
        "#0D8ECF",
        "#2A0CD0",
        "#CD0D74",
        "#CC0000",
        "#00CC00",
        "#0000CC",
        "#DDDDDD",
        "#999999",
        "#333333",
        "#990000",
    ])
    plotAreaBorderAlpha = DecimalField(default=0)
    plotAreaBorderColor = StringField(default="#000000")
    plotAreaFillAlphas = DecimalField(default=0)
    plotAreaFillColors = StringField(default="#FFFFFF")
    sequencedAnimation = BooleanField(default=True)
    startAlpha = DecimalField(default=0)
    startDuration = NumberField(default=0)
    startEffect = StringField(default="elastic")
    urlTarget = StringField(default="_self")

    def __init__(self, *args, **kwargs):
        super(amCoordinateChart, self).__init__(*args, **kwargs)
        self.graphs = []
        self.valueAxes = []

    def addGraph(self, graph):
        """Adds a graph to the chart."""
        graph.attname = graph.name + str(graph.creation_counter)
        self.graphs.insert(bisect(self.graphs, graph), copy.deepcopy(graph))

    def removeGraph(self, index):
        """Removes graph from the chart."""
        raise NotImplementedError

    def addValueAxis(self, axis):
        """
        Adds value axis to the chart. One value axis is created
        automatically, so if you don't want to change anything or add more
        value axes, you don't need to add it.

        """
        axis.attname = axis.name + str(axis.creation_counter)
        self.valueAxes.insert(bisect(self.valueAxes, axis), copy.deepcopy(axis))

    def removeValueAxis(self, index):
        """
        Removes value axis from the chart. When you remove value axis, all
        graphs assigned to this axis are also removed.

        """
        raise NotImplementedError

    def render(self, name, attrs=None):
        output = [super(amCoordinateChart, self).render(name, attrs)]

        # add valueAxis
        for axis in self.valueAxes:
            output.append(axis.render(name=axis.attname))
            output.append("%(name)s.addValueAxis(%(axis)s);" % {
                'name': name, 'axis': axis.attname})

        # add graphs
        for graph in self.graphs:
            output.append(graph.render(name=graph.attname))
            output.append("%(name)s.addGraph(%(graph)s);" % {
                'name': name, 'graph': graph.attname})

        return mark_safe(u'\n'.join(output))


class amRadarChart(amCoordinateChart):

    marginBottom = NumberField(default=0)
    marginLeft = NumberField(default=0)
    marginRight = NumberField(default=0)
    marginTop = NumberField(default=0)
    radius = StringField(default="35%")

    def get_internal_type(self):
        return "AmRadarChart"


class amRectangularChart(amCoordinateChart):

    angle = NumberField(default=0)
    autoMarginOffset = NumberField(default=10)
    autoMargins = BooleanField(default=True)
    chartCursor = InstanceField(klass=amChartCursor, null=True, readonly=False, render=False)
    chartScrollbar = InstanceField(klass=amChartScrollbar, null=True, readonly=False, render=False)
    depth3D = NumberField(default=0)
    marginBottom = NumberField(default=20)
    marginLeft = NumberField(default=20)
    marginRight = NumberField(default=20)
    marginTop = NumberField(default=20)
    marginsUpdated = BooleanField(default=False)
    plotAreaGradientAngle = NumberField(default=0)
    zoomOutButton = ObjectField(default={
        "backgroundColor": "#b2e1ff",
        "backgroundAlpha": 1,
    })
    zoomOutText = StringField(default="Show all")

    def addChartCursor(self, chartCursor):
        """Adds a ChartCursor object to a chart."""
        self.__dict__['chartCursor'] = copy.deepcopy(chartCursor)

    def removeChartCursor(self):
        """Removes cursor from the chart."""
        raise NotImplementedError

    def addChartScrollbar(self, chartScrollbar):
        """Adds a ChartScrollbar to a chart."""
        self.__dict__['chartScrollbar'] = copy.deepcopy(chartScrollbar)

    def removeChartScrollbar(self):
        """Removes scrollbar from the chart."""
        raise NotImplementedError

    def render(self, name, attrs=None):
        output = [super(amRectangularChart, self).render(name, attrs)]

        field = self._meta.get_field('chartCursor')
        if field and field.has_changed(field.get_default(), getattr(self, field.attname)):
            output.append(field.render_field(field.attname, getattr(self, field.attname)))
            output.append("%(name)s.addChartCursor(%(chartCursor)s);" % {
                'name': name, 'chartCursor': field.attname})

        field = self._meta.get_field('chartScrollbar')
        if field and field.has_changed(field.get_default(), getattr(self, field.attname)):
            output.append(field.render_field(field.attname, getattr(self, field.attname)))
            output.append("%(name)s.addChartScrollbar(%(chartScrollbar)s);" % {
                'name': name, 'chartScrollbar': field.attname})

        return mark_safe(u'\n'.join(output))


class amSerialChart(amRectangularChart):

    categoryAxis = InstanceField(klass=amCategoryAxis, null=False, readonly=True)
    categoryField = StringField()
    chartData = ArrayField(readonly=True, render=False)
    columnSpacing = NumberField(default=5)
    columnSpacing3D = NumberField(default=0)
    columnWidth = DecimalField(default=0.8)
    endDate = DateField(readonly=True, render=False)
    endIndex = NumberField(readonly=True, render=False)
    maxSelectedSeries = NumberField()
    maxSelectedTime = NumberField()
    minSelectedTime = NumberField(default=0)
    rotate = BooleanField(default=False)
    startDate = DateField(readonly=True, render=False)
    startIndex = NumberField(readonly=True, render=False)
    zoomOutOnDataUpdate = BooleanField(default=True)

    def get_internal_type(self):
        return "AmSerialChart"

    def zoomToCategoryValues(self, start, end):
	"""Zooms the chart by the value of the category axis."""
        raise NotImplementedError
    
    def zoomToDates(self, start, end):
	"""Zooms the chart from one date to another."""
        raise NotImplementedError
        
    def zoomToIndexes(self, start, end):
	"""Zooms the chart by the index of the category."""
        raise NotImplementedError


class amXYChart(amRectangularChart):

    hideXScrollbar = BooleanField(default=False)
    hideYScrollbar = BooleanField(default=False)
    maxZoomFactorIndex = NumberField(default=20)

    def get_internal_type(self):
        return "AmXYChart"
