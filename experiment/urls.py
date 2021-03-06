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
    # ex: /experiment/rule/create/
    url(r'^rule/create/(?P<pk>[0-9]+)/$', ExperimentRuleCreate.as_view(), name='experimentrule_create'),
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
    # ex: /experiment/(experiment.pk)/csv/
    url(r'^instance/(?P<pk>[0-9]+)/get/csv/$', ExperimentInstanceData.as_view(), name='experimentinstance_get_csv'),
    # ex: /experiment/(experiment.pk)/add/instance/
    url(r'^(?P<pk>[0-9]+)/add/instance/$', ExperimentInstanceAdd.as_view(), name='experimentinstance_add'),
    # ex: /experiment/api/v1/getExperiment/(foodComputerKey.pk)
    url(r'^instance/(?P<pk>[0-9]+)/add/user/$', UserExperimentInstanceAdd.as_view(), name='user_experimentinstance_add'),
    # ex: /experiment/api/v1/getExperiment/update/user
    url(r'^instance/(?P<pk>[0-9]+)/update/user/$', UserExperimentInstanceUpdate.as_view(), name='user_experimentinstance_update'),
    # ex: /experiment/getExperiment/delete/user
    url(r'^instance/(?P<pk>[0-9]+)/user/$', UserExperimentInstanceDelete.as_view(), name='user_experimentinstance_delete'),
]
