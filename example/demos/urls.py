from django.conf.urls import url

from .views import *

urlpatterns = [
    # Line & Area
    url(r'^100-stacked-area-chart/$', area100PercentStacked),
    url(r'^stacked-area-chart/$', areaStacked),
    url(r'^area-chart-with-time-based-data/$', areaWithTimeBasedData),

    # Column & Bar
    url(r'^3d-bar-chart/$', bar3D),
    url(r'^bar-and-line-chart-mix/$', barAndLineMix),
    url(r'^clustered-bar-chart/$', barClustered),
    url(r'^floating-bar-chart/$', barFloating),
    url(r'^stacked-bar-chart/$', barStacked),
    url(r'^bar-chart-with-background-image/$', barWithBackgroundImage),
    # TODO: Candlestick chart

    url(r'^100-stacked-column-chart/$', column100PercentStacked),
    url(r'^3d-column-chart/$', column3D),
    url(r'^3d-stacked-column-chart/$', column3DStacked),
    url(r'^column-and-line-chart-mix/$', columnAndLineMix),
    url(r'^column-chart-with-rotated-series/$', columnWithRotatedSeries),
    url(r'^simple-column-chart/$', columnSimple),
    url(r'^stacked-column-chart/$', columnStacked),
    url(r'^column-chart-with-gradients/$', columnWithGradient),
    url(r'^column-chart-with-images-on-top/$', columnWithImagesOnTop),

    # TODO: Smoothed line chart
]
