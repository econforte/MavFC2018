from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success
from django.http import HttpResponse
from django.core.mail import send_mail

# Imports used to serve JSON
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions

from experiment.serializers import ExperimentInstanceSerializer
from experiment.models import ExperimentInstance
from .serializers import *
from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *
import collections

import time
import csv

class PiList(View):

    @method_decorator(login_required)
    def get(self, request, parent_template=None):
        if request.user.is_staff:
            pis = Pi.objects.all()
        else:
            pis = Pi.objects.filter(user = request.user)
        return render(
            request,
            'foodcomputer/pi_list.html',
            {'pis': pis,
             'parent_template': parent_template})


class PiDetail(View):
    model = Pi
    model_name = 'Food Computer'
    template_name = 'foodcomputer/pi_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        #creating new obj variable that is just a string to print to the page
        namelist = [device.device_type.name for device in obj.devices.all()]
        actuator = {} # is the device an actuator   [name] = 0 or 1
        for device in obj.devices.all():
            if device.device_type.is_controller:
                actuator[device.device_type.name] = 1
            else:
                actuator[device.device_type.name] = 0
        time2readings = collections.defaultdict(dict)
        for device in obj.devices.all():
            for value in device.data.all():
                if not value.is_anomaly:
                    time2readings[str(value.timestamp)][device.device_type.name] = value.data_value
        prestring = "date,"+','.join(namelist) + '\n' + ','.join(["0"] + [str(actuator[x]) for x in namelist]) + '\n'
        for t in time2readings:
            temp = [t.split('+')[0]]
            for name in namelist:
                if name in time2readings[t]:
                    temp.append(str(time2readings[t][name]))
                else:
                    temp.append('NA')
            prestring += ','.join(temp) + '\n'

        return render(
            request,
            self.template_name,
            {'obj': obj,
             'prestring': prestring,
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class PiCreate(ObjectCreateMixin, View):
    form_class = PiForm
    template_name = 'foodcomputer/create_page.html'
    form_url = reverse_lazy('foodcomputer:pi_create')
    parent_template=None
    model_name = 'Food Computer'


class PiUpdate(ObjectUpdateMixin, View):
    form_class = PiForm
    model = Pi
    template_name = 'foodcomputer/update_page.html'
    parent_template=None


class PiDelete(ObjectDeleteMixin, View):
    model = Pi
    success_url = reverse_lazy('foodcomputer:piList')
    template_name = 'foodcomputer/delete_confirm.html'
    parent_template=None


class PiData(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        pi = get_object_or_404(Pi, pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="food_computer_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Device Name', 'Timestamp', 'Value', 'Is Anomily'])
        for device in pi.devices.all():
            for value in device.data.all():
                writer.writerow([value.device.device_type.name, value.timestamp, value.data_value, value.is_anomaly])
        return response



class DeviceDetail(View):
    model = Device
    model_name = 'Device'
    template_name = 'foodcomputer/device_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        #creating new obj variable that is just a string to print to the page
        data = obj.data.all()
        prestring = ""
        if len(data) > 0:
            dname = data[0].device.device_type.name
            isact = data[0].device.device_type.is_controller
            prestring = "date," + dname + '\n'
            if isact:
                prestring += "0,1\n"
            else:
                prestring += "0,0\n"
            for value in data:
                #prestring += value.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ',' + str(value.data_value) + '\n'
                prestring += str(value.timestamp).split('+')[0] + ',' + str(value.data_value) + '\n'

        return render(
            request,
            self.template_name,
            {'device': obj,
             'prestring': prestring,
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class DeviceCreate(ObjectCreateMixin, View):
    form_class = DeviceForm
    template_name = 'foodcomputer/create_page.html'
    form_url = reverse_lazy('foodcomputer:pi_create')
    parent_template = None
    model_name = 'Device'


class DeviceUpdate(ObjectUpdateMixin, View):
    form_class = DeviceForm
    model = Device
    template_name = 'foodcomputer/update_page.html'
    parent_template = None


class DeviceDelete(ObjectDeleteMixin, View):
    model = Device
    success_url = reverse_lazy('foodcomputer:piList')
    template_name = 'foodcomputer/delete_confirm.html'
    parent_template = None


class DeviceData(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="food_computer_device_'+device.device_type.name+'_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Device Name', 'Timestamp', 'Value', 'Is Anomily'])
        for value in device.data.all():
            writer.writerow([value.device.device_type.name, value.timestamp, value.data_value, value.is_anomaly])
        return response


class DeviceCurrentValueAPI(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        curVal = Data.objects.filter(device__pk=pk).latest('timestamp')
        jsonObj = dataSerializer(curVal, many=False)
        return Response(jsonObj.data)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


#----------Pi Send-------------

class initPi(APIView):
    def post(self, request):
        # Post JSON Structure
        #       {
        #           "name": "FoodComputer1",
        #           "pi_SN": "1234567890",
        #           "manual_control": true
        #       }
        serializer = PiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class initDevices(APIView):
    def post(self, request):
        # Post JSON Structure
        #       [
        #           {
        #               "pi": 1,
        #               "device_type": "Temperature Sensor",
        #               "device_ID": 123,
        #               "residual_threshold": 3.14
        #           },
        #           {
        #               "pi": 2,
        #               "device_type": "Grow Light",
        #               "device_ID": 456,
        #               "residual_threshold": .0015926
        #           }
        #       ]
        serializer = deviceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deviceData(APIView):
    def post(self, request):
        # Post JSON Structure
        #       [
        #           {
        #               "device": 1,
        #               "data_value": 13,
        #               "timestamp": "2017-02-07T15:00:00Z",
        #               "is_anomaly": true
        #           },
        #           {
        #               "device": 2,
        #               "data_value": 25,
        #               "timestamp": "2017-02-07T15:00:00Z",
        #               "is_anomaly": false
        #           }
        #       ]
        serializer = dataSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getDeviceTypes(APIView):
    def get(self, request):
        try:
            devicetypes = DeviceType.objects.all()
            serializer = deviceTypesSerializer(devicetypes, many=True)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

class anomalyEmail(APIView):
    def post(self, request):
        # Post JSON Structure
        #   {
        #       "subject": "FC1 Crashed and Burned.",
        #       "message": "It was Sean and his team of dolphins.",
        #       "frm": "FC1",
        #       "to": ["username@unomaha.edu","username2@unomaha.edu"]
        #   }
        subject = request.data.get('subject')
        message = request.data.get('message')
        frm = request.data.get('frm')
        to = request.data.get('to')
        send_mail(
            subject,
            message,
            frm,
            to,
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)


#----------Server Push-------------

class todoCheckJSON(APIView):
    # Server Push
    # Long polling idea
    def get(request, pk):
        for i in range(60):
            if something_happened():
                return http.HttpResponse()
            time.sleep(1)
        return http.HttpResponse()

class commandsJSON(APIView):
    # Server Push
    def get(request, pk):
        return HttpResponse(status=200)

class testAPI(APIView):

    def get(self, request, pk):
        pi = get_object_or_404(Pi, pk=pk)
        try:
            instance = pi.get_current_instance()
            instanceSer = ExperimentInstanceSerializer(instance, many=True)
        except ExperimentInstance.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            ctrlUpdate = ControllerUpdate.objects.filter(device__pi__pk=pk, executed=False)
            ctrlUpdateSer = ControllerUpdateSerializer(ctrlUpdate, many=True)
        except ControllerUpdate.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            piSer = PiSerializer(pi)
        except Pi.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        resp = {'pi': piSer.data,
                'controllerUpdates': ctrlUpdateSer.data,
                'instance': instanceSer.data}

        return Response(resp, status=status.HTTP_200_OK)
