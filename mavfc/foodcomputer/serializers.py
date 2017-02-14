from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, UnitType, DataType

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('pk', 'name', 'street_line_1', 'street_line_2', 'city', 'state', 'zip')
