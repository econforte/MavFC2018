from rest_framework import serializers
from .models import Address, Pi, Device, Data, DeviceType, UnitType, DataType, ControllerUpdate
from experiment.models import ExperimentInstance
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError
from django.contrib.auth.models import User
#from django.contrib.auth.models import Pi


from datetime import datetime


#Implementation
class ToDoCheckSerializer(serializers.ModelSerializer):
    # Not sure this class is needed due to boolean return
    class Meta:
        fields = ()


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('address', 'user', 'pi_SN',)


class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'


class deviceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('pk', 'name', 'model_id', 'unit_type', 'data_type', 'is_controller', 'bio_threshold',)
        depth = 1


class deviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceCurrentValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('data_value', )


class PiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pi
        fields = '__all__'


class PiPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pi
        fields = ('pk', 'pi_SN', 'manual_control',)


class ControllerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControllerUpdate
        fields = '__all__'


class emailSerializer(serializers.Serializer):
    #fields = ('pi', 'level', 'message')

    pi = serializers.IntegerField(source='data.pi', min_value=0, max_value=1000)
    level = serializers.IntegerField(source='data.level', min_value=1, max_value=3)
    message = serializers.CharField(source='data.message', allow_blank=False, max_length=1000)

    def send_mail(self):
        lvl = self.data['level']
        pk = self.data['pi']
        #Level 1 = All Admins and anyone associated to the Pi
        if (lvl == 1):
            admins = User.objects.filter(is_staff = True)
            sendList = []
            for admin in admins:
                sendList.append(admin.email)
            pk = self.data['pi']
            pi = Pi.objects.get(pk=pk)
            users = User.objects.filter(is_staff=True, pis__contains=pi, experiment_instances__experiment_instance__experiment__pi__pk=pi.pk)
            for user in users:
                sendList.append(admin.email)
        #Level 2 = All Admins and Pi User
        if (lvl == 2):
            pi = Pi.objects.get(pk=pk)
            admins = User.objects.filter(is_staff=True, pis__contains=pi)
            sendList = []
            for admin in admins:
                sendList.append(admin.email)
            #sendList.append(Pi.objects.get(pk=pk).user.objects.filter(is_active = True))
        #Level 3 = All Admins
        if (lvl == 3):
            admins = User.objects.filter(is_staff = True)
            sendList = []
            for admin in admins:
                sendList.append(admin.email)
        try:
            send_mail(
                "Pi Email",
                self.cleaned_data.get('message'),
                "Default",
                sendList,
                fail_silently=False,
            )
        except BadHeaderError:
            self.add_error(
                None,
                ValidationError(
                    'Could Not Send Email.\n'
                    'Extra headers are not allowed in email body.',
                    code='badheader'))
            return False
        else:
            return True

        #-----------------
        # body = 'Message From: {} {} at {}\nOrganization: {}\n\n{}\n'.format(
        #     self.cleaned_data.get('pi'),
        #     self.cleaned_data.get('level'),
        #     self.cleaned_data.get('message'))
        # try:
        #     # Send email (shortcut for send_mail)
        #     mail_managers(full_reason, body)
        # except BadHeaderError:
        #     self.add_error(
        #         None,
        #         ValidationError(
        #             'Could Not Send Email.\n'
        #             'Extra headers are not allowed in email body.',
        #             code='badheader'))
        #     return False
        # else:
        #     return True


class PiStateSerializer(serializers.Serializer):
    lastControllerUpdateTime = serializers.DateTimeField(required=False)
    activeInstance = serializers.IntegerField(required=False)
    pi = PiPKSerializer()

    # def update(self, instance, validated_data):
    #     instance.pi = validated_data.get('pi', instance.pi)
    #     instance.controllerUpdates = validated_data.get('controllerUpdates', instance.controllerUpdates)
    #     instance.activeInstance = validated_data.get('activeInstance', instance.activeInstance)
    #
    #
    # def updateDB(self):
    #     pi = self.data.pi
    #     ctrlUpdates = self.controllerUpdates.data
    #     if ctrlUpdates:
    #         last = ctrlUpdates[0].timestamp
    #         for ctrl in ctrlUpdates:
    #             if ctrl.timestamp > last:
    #                 last = ctrl.timestamp
    #         ControllerUpdate.objects.filter(device__pi__pk=pi.pk, executed=False, timestamp__lte=last).update(executed=True)
    #
    #     if self.activeInstance.data:
    #         activeInstance = self.activeInstance.data
    #         newActInst = ExperimentInstance.objects.get(pk=activeInstance)
    #         if not newActInst.active:
    #             actInst = pi.get_active_instance()[0]
    #             actInst.active = False
    #             actInst.save()
    #             newActInst.active = True
    #             newActInst.save()
