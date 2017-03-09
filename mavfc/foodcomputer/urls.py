from django.conf.urls import url

from .views import *

app_name = 'foodcomputer'

urlpatterns = [
#    ex: /food-computer/pi/list/
    url(r'^pi/list/$', PiList.as_view(), name='pi_list'),
    # ex: /food-computer/pi/(pi.pk)/
    url(r'^pi/(?P<pk>[0-9]+)/$', PiDetail.as_view(), name='pi_detail'),
    # ex: /food-computer/pi/create/
    url(r'^pi/create/$', PiCreate.as_view(), name='pi_create'),
    # ex: /food-computer/pi/(pi.pk)/update/
    url(r'^pi/(?P<pk>[0-9]+)/update/$', PiUpdate.as_view(), name='pi_update'),
    # ex: /food-computer/pi/(pi.pk)/delete/
    url(r'^pi/(?P<pk>[0-9]+)/delete/$', PiDelete.as_view(), name='pi_delete'),
    # ex: /food-computer/pi/(pi.pk)/get/csv/
    url(r'^pi/(?P<pk>[0-9]+)/get/csv/$', PiData.as_view(), name='pi_get_csv'),
    # ex: /food-computer/pi/(pi.pk)/document/add/
#     url(r'^pi/(?P<pk>[0-9]+)/device/add/$', .as_view(), name='device_add'),
    # ex: /food-computer/device/(device.pk)/
    url(r'^device/(?P<pk>[0-9]+)/$', DeviceDetail.as_view(), name='device_detail'),
    # ex: /food-computer/device/create/
    url(r'^device/create/$', DeviceCreate.as_view(), name='device_create'),
    # ex: /food-computer/device/(device.pk)/update/
    url(r'^device/(?P<pk>[0-9]+)/update/$', DeviceUpdate.as_view(), name='device_update'),
    # ex: /food-computer/device/(device.pk)/delete/
    url(r'^device/(?P<pk>[0-9]+)/delete/$', DeviceDelete.as_view(), name='device_delete'),
]
