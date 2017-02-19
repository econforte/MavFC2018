from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, Unittype, DataType

class experimentsSerializer(serializers.ModelSerializer):
    class Meta
        fields = ('experiment_name', 'experiment_descr', 'collection_interval')
