from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, UnitType, DataType, ControllerUpdate
from experiment.models import ExperimentInstance

from datetime import datetime

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
        fields = '__all__'

class deviceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('pk', 'name', 'model_id', 'unit_type', 'data_type', 'is_controller', 'bio_threshold')
        depth = 1

class deviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DeviceCurrentValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('data_value')

class PiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pi
        fields = '__all__'

class PiPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pi
        fields = ('pk', 'pi_SN', 'manual_control')

class ControllerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControllerUpdate
        fields = '__all__'

class emailSerializer(serializers.Serializer):
    class Meta:
        fields = ('pi', 'level', 'message')

class PiStateSerializer(serializers.Serializer):
    controllerUpdates = ControllerUpdateSerializer(many=True, required=False)
    activeInstance = serializers.IntegerField(required=False)
    pi = PiPKSerializer()

    def updateDB(self):
        pi = self.pi.data
        ctrlUpdates = self.controllerUpdates.data
        if ctrlUpdates:
            last = ctrlUpdates[0].timestamp
            for ctrl in ctrlUpdates:
                if ctrl.timestamp > last:
                    last = ctrl.timestamp
            ControllerUpdate.objects.filter(device__pi__pk=pi.pk, executed=False, timestamp__lte=last).update(executed=True)

        if self.activeInstance.data:
            activeInstance = self.activeInstance.data
            newActInst = ExperimentInstance.objects.get(pk=activeInstance)
            if not newActInst.active:
                actInst = pi.get_active_instance()[0]
                actInst.active = False
                actInst.save()
                newActInst.active = True
                newActInst.save()


