from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, UnitType, DataType

#Test Case
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('pk', 'name', 'street_line_1', 'street_line_2', 'city', 'state', 'zip')

#Implementation
class todoCheckSerializer(serializers.ModelSerializer):
    # Not sure this class is needed due to boolean return
    class Meta
        fields = ()

class keySerializer(serializers.ModelSerializer):
    class Meta
        model = Key
        fields = ('address', 'user', 'pi_SN')

class commandsSerializer(serializers.ModelSerializer):
    class Meta
        fields = ()

class sensorValuesSerializer(serializers.ModelSerializer):
    # Also not sure if this is needed due to POST
    class Meta
        model = Device
        fields = ('device', 'timestamp', 'data_value', 'is_anomaly')
