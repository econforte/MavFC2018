from django.conf.urls import url

from .views import *

app_name = 'foodcomputer'

urlpatterns = [
#    ex: /food-computer/pi/list/
    url(r'^pi/list/$', PiList.as_view(), name='piList'),
    # ex: /food-computer/pi/(pi.pk)/
    #url(r'^pi/(?P<version_key>[0-9]+)/$', VersionDetail.as_view(), name='version_detail'),
    # ex: /food-computer/pi/create/
    url(r'^pi/create/$', PiCreate.as_view(), name='pi_create'),
    # ex: /food-computer/pi/(pi.pk)/update/
    url(r'^pi/(?P<pk>[0-9]+)/update/$', PiUpdate.as_view(), name='pi_update'),
    # ex: /food-computer/pi/(pi.pk)/delete/
    url(r'^pi/(?P<pk>[0-9]+)/delete/$', PiDelete.as_view(), name='pi_delete'),
    # ex: /food-computer/pi/(pi.pk)/document/add/
#     url(r'^pi/(?P<pk>[0-9]+)/device/add/$', .as_view(), name='device_add'),
]
