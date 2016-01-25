# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import TemplateView

from uncharted.chart import *


class Area100PercentStacked(TemplateView):
    template_name = 'chart.html'

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
        graph = amGraph(type="line",
                        title="Cars",
                        valueField="cars",
                        balloonText="[[value]] ([[percents]]%)",
                        lineAlpha=0,
                        fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # second graph
        graph = amGraph(type="line",
                        title="Motorcycles",
                        valueField="motorcycles",
                        balloonText="[[value]] ([[percents]]%)",
                        lineAlpha=0,
                        fillAlphas=0.6,
        )
        chart.addGraph(graph)

        # third graph
        graph = amGraph(type="line",
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
