from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns('',
)

if 'demos.area' in settings.INSTALLED_APPS:
    urlpatterns += patterns('demos.area.views',
        url(r'100-stacked-area-chart/$', 'area100PercentStacked'),
        url(r'stacked-area-chart/$', 'areaStacked'),
        url(r'area-chart-with-time-based-data/$', 'areaWithTimeBasedData'),
    )

if 'demos.bar' in settings.INSTALLED_APPS:
    urlpatterns += patterns('demos.bar.views',
        url(r'3d-bar-chart/$', 'bar3D'),
        url(r'bar-and-line-chart-mix/$', 'barAndLineMix'),
        url(r'clustered-bar-chart/$', 'barClustered'),
        url(r'floating-bar-chart/$', 'barFloating'),
        url(r'stacked-bar-chart/$', 'barStacked'),
    )
