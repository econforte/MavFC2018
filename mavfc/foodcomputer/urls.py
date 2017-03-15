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

    # ex: /food-computer/api/v1/todo/(foodComputerKey.pk)
    url(r'^api/v1/todo/(?P<pk>[0-9]+)/$', todoCheckJSON.as_view(), name='api_device_todo'),

    # ex: /food-computer/api/v1/initpi/(piSerial.pk)
    url(r'^api/v1/initpi/$', initPi.as_view(), name='api_init_pi'),
    # ex: /food-computer/api/v1/initdevices/(piSerial.pk)
    url(r'^api/v1/initdevices/(?P<pk>[0-9]+)/$', initDevices.as_view(), name='api_init_devices'),
    # ex: /food-computer/api/v1/getCommands/(foodComputerKey.pk)
    url(r'^api/v1/getcommands/(?P<pk>[0-9]+)/$', commandsJSON.as_view(), name='api_get_device_commands'),
    # ex: /food-computer/api/v1/updatedevicedata/(data.pk)
    url(r'^api/v1/updatedevicedata/(?P<pk>[0-9]+)/$', updateDeviceData.as_view(), name='api_update_device_data'),
    # ex: /food-computer/api/v1/devicedata/([data])
    url(r'^api/v1/devicedata/$', deviceData.as_view(), name='api_device_data'),
    # ex: /food-computer/api/v1/getdevicetype/(devicetype.pk)
    url(r'^api/v1/getdevicetype/(?P<pk>[0-9]+)/$', getDeviceType.as_view(), name='api_get_device_type'),
    # ex: /food-computer/api/v1/anomalyemail/([message])
    url(r'^api/v1/anomalyemail/$', anomalyEmail.as_view(), name='api_send_anomaly_email'),
]
