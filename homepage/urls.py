from django.conf.urls import url
from .views import *

app_name = 'homepage'

urlpatterns = [
    #url(r'^$', RedirectView.as_view(pattern_name='dj-auth:pw_reset_start', permanent=False)),
    url(r'^$', Homepage.as_view(), name="homepage"),
]
