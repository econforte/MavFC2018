from django.conf.urls import url

from .views import *

app_name = 'experiment'

urlpatterns = [
    # ex: /experiment/list/
    url(r'^list/$', ExperimentList.as_view(), name='experiment_list'),

    # ex: /experiment/(experiment.pk)/
    url(r'^(?P<pk>[0-9]+)/$', ExperimentDetail.as_view(), name='experiment_detail'),

    # ex: /experiment/create/
#    url(r'^create/$', ExperimentCreate.as_view(), name='experiment_create'),

    # ex: /experiment/(experiment.pk)/update/
#    url(r'^(?P<pk>[0-9]+)/update/$', ExperimentUpdate.as_view(), name='experiment_update'),

    # ex: /experiment/(experiment.pk)/delete/
#    url(r'^(?P<pk>[0-9]+)/delete/$', ExperimentDelete.as_view(), name='experiment_delete'),

]