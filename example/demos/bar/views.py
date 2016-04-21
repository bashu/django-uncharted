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
        # first graph
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
        # first graph
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
