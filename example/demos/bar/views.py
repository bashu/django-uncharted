# -*- coding: utf-8 -*-

# from random import random
# from datetime import timedelta

from django.conf import settings
# from django.utils import timezone
from django.views.generic import TemplateView

from uncharted.chart import *


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
