import re

from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('demos.urls')),
]
