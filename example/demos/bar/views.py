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

