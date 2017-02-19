from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, Unittype, DataType

class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('experiment_name', 'experiment_descr', 'collection_interval')
