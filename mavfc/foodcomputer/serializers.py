from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, UnitType, DataType

#Test Case
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('pk', 'name', 'street_line_1', 'street_line_2', 'city', 'state', 'zip')

#Implementation
class ToDoCheckSerializer(serializers.ModelSerializer):
    # Not sure this class is needed due to boolean return
    class Meta:
        fields = ()

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('address', 'user', 'pi_SN')

class CommandsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ()

class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('device', 'timestamp', 'data_value', 'is_anomaly')

class deviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('pi', 'device_type', 'device_id', 'upper_threshold', 'lower_threshold')
