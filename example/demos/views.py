# -*- coding: utf-8 -*-

from random import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.views.generic import TemplateView

from uncharted.chart import *


class Area100PercentStacked(TemplateView):
    template_name = 'area/chart.html'

    chartData = [
        {
            'year': 2000,
            'cars': 1587,
            'motorcycles': 650,
            'bicycles': 121
        }, {
            'year': 1995,
            'cars': 1567,
            'motorcycles': 683,
            'bicycles': 146
        }, {
            'year': 1996,
            'cars': 1617,
            'motorcycles': 691,
            'bicycles': 138
        }, {
            'year': 1997,
            'cars': 1630,
            'motorcycles': 642,
            'bicycles': 127
        }, {
            'year': 1998,
            'cars': 1660,
            'motorcycles': 699,
            'bicycles': 105
        }, {
            'year': 1999,
            'cars': 1683,
            'motorcycles': 721,
            'bicycles': 109
        }, {
            'year': 2000,
            'cars': 1691,
            'motorcycles': 737,
            'bicycles': 112
        }, {
            'year': 2001,
            'cars': 1298,
            'motorcycles': 680,
            'bicycles': 101
        }, {
            'year': 2002,
            'cars': 1275,
            'motorcycles': 664,
            'bicycles': 97
        }, {
            'year': 2003,
            'cars': 1246,
            'motorcycles': 648,
            'bicycles': 93
        }, {
            'year': 2004,
            'cars': 1218,
            'motorcycles': 637,
            'bicycles': 101
        }, {
            'year': 2005,
            'cars': 1213,
            'motorcycles': 633,
            'bicycles': 87
        }, {
            'year': 2006,
            'cars': 1199,
            'motorcycles': 621,
            'bicycles': 79
        }, {
            'year': 2007,
            'cars': 1110,
            'motorcycles': 210,
            'bicycles': 81
        }, {
            'year': 2008,
            'cars': 1165,
            'motorcycles': 232,
            'bicycles': 75
        }, {
            'year': 2009,
            'cars': 1145,
            'motorcycles': 219,
            'bicycles': 88
        }, {
            'year': 2010,
            'cars': 1163,
            'motorcycles': 201,
            'bicycles': 82
        }, {
            'year': 2011,
            'cars': 1180,
            'motorcycles': 285,
            'bicycles': 87
        }, {
            'year': 2012,
            'cars': 1159,
            'motorcycles': 277,
            'bicycles': 71
        }]
    
    def get_context_data(self, *args, **kwargs):
        context = super(Area100PercentStacked, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="year",
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )

        chart.zoomOutButton = {
            'backgroundColor': "#000000",
            'backgroundAlpha': 0.15,
        }
        
        chart.addTitle("Traffic incidents per year", 15)

        # AXES
        # Category
        chart.categoryAxis.gridAlpha = 0.07
        chart.categoryAxis.axisColor = "#DADADA"
        chart.categoryAxis.startOnAxis = True

        # Value
        valueAxis = amValueAxis(title="percent", stackType="100%", gridAlpha=0.07)
        chart.addValueAxis(valueAxis)

        # GRAPHS
        # first graph
        graph = amGraph(
            type="line",
            title="Cars",
            valueField="cars",
            balloonText="[[value]] ([[percents]]%)",
            lineAlpha=0,
            fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # second graph
        graph = amGraph(
            type="line",
            title="Motorcycles",
            valueField="motorcycles",
            balloonText="[[value]] ([[percents]]%)",
            lineAlpha=0,
            fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # third graph
        graph = amGraph(
            type="line",
            title="Bicycles",
            valueField="bicycles",
            balloonText="[[value]] ([[percents]]%)",
            lineAlpha=0,
            fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # LEGEND
        legend = amLegend(align="center")
        chart.addLegend(legend)

        # CURSOR
        chartCursor = amChartCursor(zoomable=False, cursorAlpha=0)
        chart.addChartCursor(chartCursor)

        context['chart'] = chart
        return context

area100PercentStacked = Area100PercentStacked.as_view()


class AreaStacked(Area100PercentStacked):

    def get_context_data(self, *args, **kwargs):
        context = super(AreaStacked, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            marginTop=10,
            dataProvider=self.chartData,
            categoryField="year",
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )

        chart.zoomOutButton = {
            'backgroundColor': "#000000",
            'backgroundAlpha': 0.15,
        }

        # AXES
        # Category
        chart.categoryAxis.gridAlpha = 0.07
        chart.categoryAxis.axisColor = "#DADADA"
        chart.categoryAxis.startOnAxis = True

        # Value
        valueAxis = amValueAxis(
            title="Traffic incidents",
            stackType="regular",  # this line makes the chart "stacked"
            gridAlpha=0.07,
        )
        chart.addValueAxis(valueAxis)

        # GUIDES are vertical (can also be horizontal) lines (or areas) marking some event.
        # first guide
        guide1 = amGuide(
            category="2001",
            lineColor="#CC0000",
            lineAlpha=1,
            dashLength=2,
            inside=True,
            labelRotation=90,
            label="fines for speeding increased",
        )
        chart.categoryAxis.addGuide(guide1);

        # second guide
        guide2 = amGuide(
            category="2007",
            lineColor="#CC0000",
            lineAlpha=1,
            dashLength=2,
            inside=True,
            labelRotation=90,
            label="motorcycle maintenance fee introduced",
        )
        chart.categoryAxis.addGuide(guide2);

        # GRAPHS
        # first graph
        graph = amGraph(
            type="line",
            title="Cars",
            valueField="cars",
            balloonText="[[value]] ([[percents]]%)",
            lineAlpha=1,
            fillAlphas=0.6,  # setting fillAlphas to > 0 value makes it area graph
            hidden=True,
        )
        chart.addGraph(graph)

        # second graph
        graph = amGraph(
            type="line",
            title="Motorcycles",
            valueField="motorcycles",
            balloonText="[[value]] ([[percents]]%)",
            lineAlpha=1,
            fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # third graph
        graph = amGraph(
            type="line",
            title="Bicycles",
            valueField="bicycles",
            balloonText="[[value]] ([[percents]]%)",
            lineAlpha=1,
            fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # LEGEND
        legend = amLegend(position="top")
        chart.addLegend(legend)

        # CURSOR
        chartCursor = amChartCursor(zoomable=False, cursorAlpha=0)
        chart.addChartCursor(chartCursor)

        context['chart'] = chart
        return context

areaStacked = AreaStacked.as_view()


class AreaWithTimeBasedData(Area100PercentStacked):

    @property
    def chartData(self):
        output = []
        d = timezone.now() - timedelta(minutes=1000)
        for i in xrange(0, 1000):
            d = d + timedelta(minutes=1)
            value = int((random() * 40) + 10)
            output.append({
                'date': d,#.isoformat(),
                'visits': value,
            })
        return output

    def get_context_data(self, *args, **kwargs):
        context = super(AreaWithTimeBasedData, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            marginRight=30,
            dataProvider=self.chartData,
            categoryField="date",
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )

        chart.zoomOutButton = {
            'backgroundColor': "#000000",
            'backgroundAlpha': 0.15,
        }

        chart.addListener("dataUpdated", "zoomChart");

        # AXES
        # Category
        chart.categoryAxis.parseDates = True
        chart.categoryAxis.minPeriod = "mm"
        chart.categoryAxis.gridAlpha = 0.07
        chart.categoryAxis.axisColor = "#DADADA"

        # Value
        valueAxis = amValueAxis(
            title="Unique visitors",
            gridAlpha=0.07,
        )
        chart.addValueAxis(valueAxis)

        # GRAPHS
        # first graph
        graph = amGraph(
            type="line",
            title="red line",
            valueField="visits",
            lineAlpha=1,
            lineColor="#d1cf2a",
            fillAlphas=0.3,  # setting fillAlphas to > 0 value makes it area graph
        )
        chart.addGraph(graph)

        # CURSOR
        chartCursor = amChartCursor(
            cursorPosition="mouse",
            categoryBalloonDateFormat="JJ:NN, DD MMMM",
        )
        chart.addChartCursor(chartCursor)

        # SCROLLBAR
        chartScrollbar = amChartScrollbar()
        chart.addChartScrollbar(chartScrollbar)

        context['chart'] = chart
        return context

areaWithTimeBasedData = AreaWithTimeBasedData.as_view()


class Bar3D(TemplateView):
    template_name = 'bar/chart.html'

    chartData = [
        {
            'year': 2005,
            'income': 23.5
        }, {
            'year': 2006,
            'income': 26.2
        }, {
            'year': 2007,
            'income': 30.1
        }, {
            'year': 2008,
            'income': 29.5
        }, {
            'year': 2009,
            'income': 24.6
        }]
    
    def get_context_data(self, *args, **kwargs):
        context = super(Bar3D, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="year",
            rotate=True,
            depth3D=20,
            angle=30,
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )
        
        # AXES
        # Category
        chart.categoryAxis.gridPosition = "start"
        chart.categoryAxis.axisColor = "#DADADA"
        chart.categoryAxis.fillAlpha = 1
        chart.categoryAxis.gridAlpha = 0
        chart.categoryAxis.fillColor = "#FAFAFA"
        
        # Value
        valueAxis = amValueAxis(title="Income in millions, USD", axisColor="#DADADA", gridAlpha=0.1)
        chart.addValueAxis(valueAxis)

        # GRAPHS
        graph = amGraph(
            type="column",
            title="Income",
            valueField="income",
            balloonText="Income in [[category]]:[[value]]",
            lineAlpha=0,
            fillColors=["#bf1c25"],
            fillAlphas=1,
        )
        chart.addGraph(graph)

        context['chart'] = chart
        return context

bar3D = Bar3D.as_view()


class BarAndLineMix(Bar3D):

    chartData = [
        {
            'year': 2005,
            'income': 23.5,
            'expenses': 18.1
        }, {
            'year': 2006,
            'income': 26.2,
            'expenses': 22.8
        }, {
            'year': 2007,
            'income': 30.1,
            'expenses': 23.9
        }, {
            'year': 2008,
            'income': 29.5,
            'expenses': 25.1
        }, {
            'year': 2009,
            'income': 24.6,
            'expenses': 25.0
        }]
    
    def get_context_data(self, *args, **kwargs):
        context = super(BarAndLineMix, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="year",
            startDuration=1,
            rotate=True,
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )
        
        # AXES
        # Category
        chart.categoryAxis.gridPosition = "start"
        chart.categoryAxis.axisColor = "#DADADA"
        chart.categoryAxis.dashLength = 5
        
        # Value
        valueAxis = amValueAxis(
            title="Million USD",
            dashLength=5,
            axisAlpha=0.2,
            position="top",
        )
        chart.addValueAxis(valueAxis)

        # GRAPHS
        # column graph
        graph1 = amGraph(
            type="column",
            title="Income",
            valueField="income",
            lineAlpha=0,
            fillColors=["#ADD981"],
            fillAlphas=1,
        )
        chart.addGraph(graph1)

        # line graph
        graph2 = amGraph(
            type="line",
            title="Expenses",
            valueField="expenses",
            lineThickness=2,
            bullet="round",
            fillAlphas=0,
        )
        chart.addGraph(graph2)

        # LEGEND
        legend = amLegend()
        chart.addLegend(legend)
        
        context['chart'] = chart
        return context

barAndLineMix = BarAndLineMix.as_view()


class BarClustered(BarAndLineMix):

    def get_context_data(self, *args, **kwargs):
        context = super(BarClustered, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="year",
            startDuration=1,
            plotAreaBorderColor="#DADADA",
            plotAreaBorderAlpha=1,
            rotate=True,
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )
        
        # AXES
        # Category
        chart.categoryAxis.gridPosition = "start"
        chart.categoryAxis.gridAlpha = 0.1
        chart.categoryAxis.axisAlpha = 0
        
        # Value
        valueAxis = amValueAxis(
            axisAlpha=0,
            gridAlpha=0.1,
            position="top",
        )
        chart.addValueAxis(valueAxis)

        # GRAPHS
        # first graph
        graph1 = amGraph(
            type="column",
            title="Income",
            valueField="income",
            balloonText="Income:[[value]]",
            lineAlpha=0,
            fillColors=["#ADD981"],
            fillAlphas=1,
        )
        chart.addGraph(graph1)

        # second graph
        graph2 = amGraph(
            type="column",
            title="Expenses",
            valueField="expenses",
            balloonText="Expenses:[[value]]",
            lineAlpha=0,
            fillColors=["#81acd9"],
            fillAlphas=1,
        )
        chart.addGraph(graph2)

        # LEGEND
        legend = amLegend()
        chart.addLegend(legend)

        context['chart'] = chart
        return context

barClustered = BarClustered.as_view()


class BarFloating(BarClustered):
    template_name = 'area/chart.html'

    chartData = [
        {
            'name': "John",
            'startTime': 8,
            'endTime': 11,
            'color': "#FF0F00"
        }, {
            'name': "Joe",
            'startTime': 10,
            'endTime': 13,
            'color': "#FF9E01"
        }, {
            'name': "Susan",
            'startTime': 11,
            'endTime': 18,
            'color': "#F8FF01"
        }, {
            'name': "Eaton",
            'startTime': 15,
            'endTime': 19,
            'color': "#04D215"
        }]

    def get_context_data(self, *args, **kwargs):
        context = super(BarFloating, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="name",
            startDuration=1,
            columnWidth=0.9,
            rotate=True,
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )
        
        # AXES
        # Category
        chart.categoryAxis.gridPosition = "start"
        chart.categoryAxis.gridAlpha = 0.1
        chart.categoryAxis.axisAlpha = 0
        
        # Value
        valueAxis = amValueAxis(
            axisAlpha=0,
            gridAlpha=0.1,
            unit=":00",
        )
        chart.addValueAxis(valueAxis)

        # GRAPHS
        graph1 = amGraph(
            type="column",
            valueField="endTime",
            openField="startTime",
            balloonText="Income:[[value]]",
            lineAlpha=0,
            colorField="color",
            fillAlphas=0.8,
        )
        chart.addGraph(graph1)

        context['chart'] = chart
        return context

barFloating = BarFloating.as_view()


class BarStacked(BarFloating):
    template_name = 'bar/3d.html'

    chartData = [
        {
            'year': "2003",
            'europe': 2.5,
            'namerica': 2.5,
            'asia': 2.1,
            'lamerica': 0.3,
            'meast': 0.2,
            'africa': 0.1
        }, {
            'year': "2004",
            'europe': 2.6,
            'namerica': 2.7,
            'asia': 2.2,
            'lamerica': 0.3,
            'meast': 0.3,
            'africa': 0.1
        }, {
            'year': "2005",
            'europe': 2.8,
            'namerica': 2.9,
            'asia': 2.4,
            'lamerica': 0.3,
            'meast': 0.3,
            'africa': 0.1
        }]

    def get_context_data(self, *args, **kwargs):
        context = super(BarStacked, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="year",
            plotAreaBorderAlpha=0.2,
            rotate=True,
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )
        
        # AXES
        # Category
        chart.categoryAxis.gridPosition = "start"
        chart.categoryAxis.gridAlpha = 0.1
        chart.categoryAxis.axisAlpha = 0
        
        # Value
        valueAxis = amValueAxis(
            axisAlpha=0,
            gridAlpha=0.1,
            stackType="regular",
        )
        chart.addValueAxis(valueAxis)

        # GRAPHS
        # first graph
        graph1 = amGraph(
            type="column",
            title="Europe",
            labelText="[[value]]",
            valueField="europe",
            lineAlpha=0,
            fillAlphas=1,
            lineColor="#C72C95",
        )
        chart.addGraph(graph1)

        # second graph
        graph2 = amGraph(
            type="column",
            title="North America",
            labelText="[[value]]",
            valueField="namerica",
            lineAlpha=0,
            fillAlphas=1,
            lineColor="#D8E0BD",
        )
        chart.addGraph(graph2)

        # third graph
        graph3 = amGraph(
            type="column",
            title="Asia-Pacific",
            labelText="[[value]]",
            valueField="asia",
            lineAlpha=0,
            fillAlphas=1,
            lineColor="#B3DBD4",
        )
        chart.addGraph(graph3)

        # forth graph
        graph4 = amGraph(
            type="column",
            title="Latin America",
            labelText="[[value]]",
            valueField="lamerica",
            lineAlpha=0,
            fillAlphas=1,
            lineColor="#69A55C",
        )
        chart.addGraph(graph4)

        # fifth graph
        graph5 = amGraph(
            type="column",
            title="Middle-East",
            labelText="[[value]]",
            valueField="meast",
            lineAlpha=0,
            fillAlphas=1,
            lineColor="#B5B8D3",
        )
        chart.addGraph(graph5)

        # sixth graph
        graph6 = amGraph(
            type="column",
            title="Africa",
            labelText="[[value]]",
            valueField="africa",
            lineAlpha=0,
            fillAlphas=1,
            lineColor="#F4E23B",
        )
        chart.addGraph(graph6)

        # LEGEND
        legend = amLegend()
        legend.position = "right"
        legend.borderAlpha = 0.3
        legend.horizontalGap = 10
        legend.switchType = "v"
        chart.addLegend(legend)

        context['chart'] = chart
        return context

barStacked = BarStacked.as_view()


class BarWithBackgroundImage(BarStacked):
    template_name = 'bar/bg.html'

    chartData = [
        {
            'country': "Czech Republic",
            'litres': 156.90,
            'short': "CZ"
        }, {
            'country': "Ireland",
            'litres': 131.10,
            'short': "IR"
        }, {
            'country': "Germany",
            'litres': 115.80,
            'short': "DE"
        }, {
            'country': "Australia",
            'litres': 109.90,
            'short': "AU"
        }, {
            'country': "Austria",
            'litres': 108.30,
            'short': "AT"
        }, {
            'country': "UK",
            'litres': 99.00,
            'short': "UK"
        }, {
            'country': "Belgium",
            'litres': 93.00,
            'short': "BE"
        }]

    def get_context_data(self, *args, **kwargs):
        context = super(BarWithBackgroundImage, self).get_context_data(*args, **kwargs)

        chart = amSerialChart(
            name='chart',
            dataProvider=self.chartData,
            categoryField="country",
            color="#FFFFFF",
            rotate=True,
            pathToImages="%samcharts2/amcharts/images/" % settings.STATIC_URL,
        )

        # this line makes the chart to show image in the background
        chart.backgroundImage = "%simages/bg.jpg" % settings.STATIC_URL
        
        # sometimes we need to set margins manually
        # autoMargins should be set to false in order chart to use custom margin values 
        chart.autoMargins = False
        chart.marginTop = 100
        chart.marginLeft = 50
        chart.marginRight = 30
        chart.startDuration = 2
                
        # AXES
        # Category
        chart.categoryAxis.labelsEnabled = False
        chart.categoryAxis.gridAlpha = 0
        chart.categoryAxis.axisAlpha = 0
        
        # Value
        valueAxis = amValueAxis(
            axisAlpha=0,
            gridAlpha=0,
            labelsEnabled=False,
            minimum=0,
        )
        chart.addValueAxis(valueAxis)

        # GRAPHS
        graph = amGraph(
            type="column",
            valueField="litres",
            lineAlpha=0,
            fillAlphas=0.5,
            # you can pass any number of colors in array to create more fancy gradients
            fillColors=["#000000", "#FF6600"],
            gradientOrientation="horizontal",
            labelPosition="bottom",
            labelText="[[category]]: [[value]] Litres",
            balloonText="[[category]]: [[value]] Litres",
        )
        chart.addGraph(graph)

        # LABEL
        chart.addLabel(50, 40, "Beer Consumption by country", "left", 15, "#000000", 0, 1, True);

        context['chart'] = chart
        return context

barWithBackgroundImage = BarWithBackgroundImage.as_view()
