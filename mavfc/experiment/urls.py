from django.conf.urls import url

from .views import *

app_name = 'experiment'

urlpatterns = [
    # ex: /product/list/
    #url(r'^list/$', ProductList.as_view(), name='productList'),

    # ex: /experiment/api/getExperiment/(foodComputerKey.pk)
    url(r'^api/getExperiment/(?P<pk>[0-9]+)/$', experimentJSON),
]
