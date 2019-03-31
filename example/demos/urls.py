from django.conf.urls import url

from .views import *

urlpatterns = [
    # area
    url(r'^100-stacked-area-chart/$', area100PercentStacked),
    url(r'^stacked-area-chart/$', areaStacked),
    url(r'^area-chart-with-time-based-data/$', areaWithTimeBasedData),

    # bar
    url(r'^3d-bar-chart/$', bar3D),
    url(r'^bar-and-line-chart-mix/$', barAndLineMix),
    url(r'^clustered-bar-chart/$', barClustered),
    url(r'^floating-bar-chart/$', barFloating),
    url(r'^stacked-bar-chart/$', barStacked),
    url(r'^bar-chart-with-background-image/$', barWithBackgroundImage),
    # TODO: Candlestick chart
]
