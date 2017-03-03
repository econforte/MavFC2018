from django.conf.urls import url

from .views import *

app_name = 'experiment'

urlpatterns = [
    # ex: /experiment/search/
    url(r'^search/$', ExperimentSearch.as_view(), name='experiment_search'),
    # ex: /experiment/list/
    url(r'^list/$', ExperimentList.as_view(), name='experiment_list'),
    # ex: /experiment/(experiment.pk)/
    url(r'^(?P<pk>[0-9]+)/$', ExperimentDetail.as_view(), name='experiment_detail'),
    # ex: /experiment/create/
    url(r'^create/$', ExperimentCreate.as_view(), name='experiment_create'),
    # ex: /experiment/(experiment.pk)/update/
    url(r'^(?P<pk>[0-9]+)/update/$', ExperimentUpdate.as_view(), name='experiment_update'),
    # ex: /experiment/(experiment.pk)/delete/
    url(r'^(?P<pk>[0-9]+)/delete/$', ExperimentDelete.as_view(), name='experiment_delete'),
    # ex: /experiment/(experiment.pk)/
    url(r'^rule/(?P<pk>[0-9]+)/$', ExperimentRuleDetail.as_view(), name='experimentrule_detail'),
    # ex: /experiment/create/
    url(r'^rule/create/$', ExperimentRuleCreate.as_view(), name='experimentrule_create'),
    # ex: /experiment/(experiment.pk)/update/
    url(r'^rule/(?P<pk>[0-9]+)/update/$', ExperimentRuleUpdate.as_view(), name='experimentrule_update'),
    # ex: /experiment/(experiment.pk)/delete/
    url(r'^rule/(?P<pk>[0-9]+)/delete/$', ExperimentRuleDelete.as_view(), name='experimentrule_delete'),
    # ex: /experiment/(experiment.pk)/
    url(r'^instance/(?P<pk>[0-9]+)/$', ExperimentInstanceDetail.as_view(), name='experimentinstance_detail'),
    # ex: /experiment/create/
    url(r'^instance/create/$', ExperimentInstanceCreate.as_view(), name='experimentinstance_create'),
    # ex: /experiment/(experiment.pk)/update/
    url(r'^instance/(?P<pk>[0-9]+)/update/$', ExperimentInstanceUpdate.as_view(), name='experimentinstance_update'),
    # ex: /experiment/(experiment.pk)/delete/
    url(r'^instance/(?P<pk>[0-9]+)/delete/$', ExperimentInstanceDelete.as_view(), name='experimentinstance_delete'),
]