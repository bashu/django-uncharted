from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns('',
)

if 'demos.area' in settings.INSTALLED_APPS:
    urlpatterns = patterns('demos.area.views',
        url(r'100-stacked-area-chart/$', 'area100PercentStacked'),
        url(r'stacked-area-chart/$', 'areaStacked'),
        url(r'area-chart-with-time-based-data/$', 'areaWithTimeBasedData'),

    )
