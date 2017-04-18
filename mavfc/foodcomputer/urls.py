from django.conf.urls import url

from .views import *

app_name = 'foodcomputer'

urlpatterns = [
    # ex: /food-computer/pi/list/
    url(r'^pi/list/$', PiList.as_view(), name='pi_list'),
    # ex: /food-computer/pi/(pi.pk)/
    url(r'^pi/(?P<pk>[0-9]+)/$', PiDetail.as_view(), name='pi_detail'),
    # ex:/food-computer/pi/(pi.pk)/chart/
    url(r'^pi/(?P<pk>[0-9]+)/chart/$', PiChart.as_view(), name='pi_chart'),
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
    # ex: /food-computer/pi/(pi.pk)/get/csv/
    url(r'^device/(?P<pk>[0-9]+)/get/csv/$', DeviceData.as_view(), name='device_get_csv'),
    # ex: /food-computer/api/v1/sensorValues/(foodComputerKey.pk, [data])
    url(r'^api/v1/device/(?P<pk>[0-9]+)/current/value/$', DeviceCurrentValueAPI.as_view(), name='api_device_current_value'),
    # ex: /food-computer/api/v1/pi/(foodComputerKey.pk)/current/value/
    url(r'^api/v1/pi/(?P<pk>[0-9]+)/current/value/$', PiCurrentValueAPI.as_view(), name='api_pi_current_value'),
    # ex: /food-computer/address/(address.pk)/delete/
    url(r'^(?P<pk>[0-9]+)/address/add/$', AddressAdd.as_view(), name='address_add'),
    # ex: /food-computer/address/(address.pk)/delete/
    url(r'^address/(?P<pk>[0-9]+)/update/$', AddressUpdate.as_view(), name='address_update'),
    # ex: /food-computer/address/(address.pk)/delete/
    url(r'^address/(?P<pk>[0-9]+)/delete/$', AddressDelete.as_view(), name='address_delete'),

    #----------Pi Send-------------
    # ex: /food-computer/api/v1/initpi/(piSerial.pk)
    url(r'^api/v1/initpi/$', initPi.as_view(), name='api_init_pi'),
    # ex: /food-computer/api/v1/initdevices/(piSerial.pk)
    url(r'^api/v1/initdevices/$', initDevices.as_view(), name='api_init_devices'),
    # ex: /food-computer/api/v1/devicedata/([data])
    url(r'^api/v1/devicedata/$', deviceData.as_view(), name='api_device_data'),
    # ex: /food-computer/api/v1/getdevicetype/(devicetype.pk)
    url(r'^api/v1/getdevicetypes/$', getDeviceTypes.as_view(), name='api_get_device_types'),
    # ex: /food-computer/api/v1/anomalyemail/([message])
    url(r'^api/v1/anomalyemail/$', anomalyEmail.as_view(), name='api_send_anomaly_email'),

    #----------Server Push-------------
    # ex: /food-computer/api/v1/todo/(foodComputerKey.pk)
    url(r'^api/v1/push/(?P<pk>[0-9]+)/$', ServerPushAPI.as_view(), name='api_pi_push'),
    # ex: /food-computer/api/v1/getCommands/(foodComputerKey.pk)
    url(r'^api/v1/test/(?P<pk>[0-9]+)/$', testAPI.as_view(), name='api_test'),
]
