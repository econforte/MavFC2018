from django.conf.urls import url

from .views import *

app_name = 'experiment'

urlpatterns = [
    # ex: /experiment/list/
    url(r'^list/$', ExperimentList.as_view(), name='experimentList'),
    # ex: /experiment/(pi.pk)/
    url(r'^(?P<pk>[0-9]+)/$', ExperimentDetail.as_view(), name='experiment_detail'),
]