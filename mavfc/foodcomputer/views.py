from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
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
from .utils import ChartDataPreparation, DownloadDataPreparation, DeviceDataPreparation
from .models import *
from .forms import *

import collections
import math
import datetime

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
        
        cdp = ChartDataPreparation()
        namelist = cdp.getNameList(obj)
        isActuator = cdp.getActuatorDictionary(obj)
        time2sensor = cdp.initializeDataValues(obj)
        time2sensor = cdp.subsetDataValues(time2sensor, 200)
        prestring = cdp.constructTable(time2sensor, namelist, isActuator)

        return render(
            request,
            self.template_name,
            {'obj': obj,
             'prestring': prestring,
             'height': '700px',
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class PiChart(View):
    model = Pi
    model_name = 'Food Computer Chart'
    template_name = 'foodcomputer/pi_data_page.html'
    parent_template = None
    
    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form_class = AdvancedOptionsForm(request=request, pk=pk)
        
        cdp = ChartDataPreparation()
        namelist = cdp.getNameList(obj)
        isActuator = cdp.getActuatorDictionary(obj)
        time2sensor = cdp.initializeDataValues(obj)
        time2sensor = cdp.subsetDataValues(time2sensor, 200)
        prestring = cdp.constructTable(time2sensor, namelist, isActuator)
        
        return render(\
                      request,\
                      self.template_name,\
                      {'obj':                   obj,\
                       'prestring':             prestring,\
                       'height':                '700px',\
                       'form_url':              reverse("foodcomputer:pi_chart", kwargs={'pk':pk}),\
                       'advanced_options_form': form_class,\
                       'model_name':            self.model_name,\
                       'parent_template':       self.parent_template})
    
    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form_class = AdvancedOptionsForm(request.POST, request=request, pk=pk)
        cdp = ChartDataPreparation()
        height = '700px'
        
        if form_class.is_valid():
            cdp = ChartDataPreparation(start_date=datetime.datetime.strptime(form_class.cleaned_data['start_date'], '%Y-%m-%dT%H:%M'),\
                                       end_date=datetime.datetime.strptime(form_class.cleaned_data['end_date'], '%Y-%m-%dT%H:%M'),\
                                       show_anomalies=form_class.cleaned_data['show_anomalies'],
                                       sensors=form_class.cleaned_data['devices'])
                                       
        namelist = cdp.getNameList(obj)
        isActuator = cdp.getActuatorDictionary(obj)
        if not 0 in [isActuator[x] for x in isActuator]: height = "200px"
        time2sensor = cdp.initializeDataValues(obj)
        time2sensor = cdp.subsetDataValues(time2sensor, 200)
        prestring = cdp.constructTable(time2sensor, namelist, isActuator)
            
        return render(\
                      request,\
                      self.template_name,\
                      {'obj':                   obj,\
                       'prestring':             prestring,\
                       'height':                height,\
                       'form_url':              reverse("foodcomputer:pi_chart", kwargs={'pk':pk}),\
                       'advanced_options_form': form_class,\
                       'model_name':            self.model_name,\
                       'parent_template':       self.parent_template})
            
            
        
        
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
    model_name = 'Food Computer'


class PiDelete(ObjectDeleteMixin, View):
    model = Pi
    success_url = reverse_lazy('foodcomputer:pi_list')
    template_name = 'foodcomputer/delete_confirm.html'
    parent_template=None
    model_name = 'Food Computer'


class PiData(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        pi = get_object_or_404(Pi, pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="food_computer_data.csv"'
        writer = csv.writer(response, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(['Device Name', 'Timestamp', 'Value', 'Is Anomily'])
        
        ddp = DownloadDataPreparation(pi)
        writer.writerow(ddp.firstline(pi))
        writer.writerow(ddp.secondline(pi))
        time2sensor = ddp.initializeDataValues(pi)
        for linelist in ddp.downloadFileGenerator(time2sensor):
            writer.writerow(linelist)
        return response
    

class DeviceDetail(View):
    model = Device
    model_name = 'Device'
    template_name = 'foodcomputer/device_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        height = "700px"

        ddp = DeviceDataPreparation(obj)
        time2sensor = ddp.initializeDeviceDataValues(obj)
        time2sensor = ddp.subsetDataValues(time2sensor)
        prestring = ddp.constructTable(time2sensor, numdp=200)
        
        if obj.device_type.is_controller:
            height = "200xp"

        return render(
            request,
            self.template_name,
            {'device': obj,
             'prestring': prestring,
             'height': height,
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
    model_name = 'Device'


class DeviceDelete(ObjectDeleteMixin, View):
    model = Device
    success_url = reverse_lazy('foodcomputer:pi_list')
    template_name = 'foodcomputer/delete_confirm.html'
    parent_template = None
    model_name = 'Device'


class DeviceData(View):

    @method_decorator(login_required)
    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="food_computer_device_'+device.device_type.name+'_data.csv"'
        writer = csv.writer(response)
        writer.writerow(['Device Name', 'Date', 'Value', 'Is Anomily'])
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
        #       "pi": 1,
        #       "level": 1,
        #       "message": "It was Sean and his team of dolphins."
        #   }
        serializer = emailSerializer(data=request.data)
        if serializer.is_valid():
            lvl = request.data.get('level')
            #Level 1 = All Admins and anyone associated to the Pi
            if (lvl == 1):
                admins = user.objects.filter(is_staff = True)
                sendList = []
                for admin in admins:
                    sendList.append(admin.email())
                users = Pi.objects.get(pk=pk).user()
                for user in users:
                    sendList.append(user.email())
            #Level 2 = All Admins and Pi User
            if (lvl == 2):
                admins = User.objects.filter(is_staff = True)
                sendList = []
                for admin in admins:
                    sendList.append(admin.email())
                #sendList.append(Pi.objects.get(pk=pk).user.objects.filter(is_active = True))
            #Level 3 = All Admins
            if (lvl == 3):
                admins = User.objects.filter(is_staff = True)
                sendList = []
                for admin in admins:
                    sendList.append(admin.email())
            send_mail(
                "Pi Email",
                request.data.get('message'),
                "Default",
                sendList,
                fail_silently=False,
            )
            return Response("Email(s) Sent")
        else: return Response("No Email(s) Sent")


#----------Server Push-------------

class ServerPushAPI(APIView):
    # Server Push
    # Long polling idea
    def post(self, request, pk):
        serializer = PiStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.updateDB()
            # Generate Push Response
            resp = {}
            pi = get_object_or_404(Pi, pk=pk)
            endInstance = pi.get_end_instance()
            activeInstance = pi.get_active_instance()
            startInstance = pi.get_start_instance()
            try:
                endInstanceSer = ExperimentInstanceSerializer(endInstance, many=True)
                activeInstanceSer = ExperimentInstanceSerializer(activeInstance, many=True)
                startInstanceSer = ExperimentInstanceSerializer(startInstance, many=True)
            except ExperimentInstance.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if endInstance:
                resp['endInstance'] = endInstanceSer.data
            if activeInstance:
                resp['activeInstance'] = activeInstanceSer.data
            if startInstance:
                resp['startInstance'] = startInstanceSer.data

            if pi.manual_control and startInstance:
                pi.manual_control = False
                pi.save()
            elif (not pi.manual_control) and (not startInstance) and endInstance:
                pi.manual_control = True
                pi.save()

            try:
                piSer = PiSerializer(pi)
            except Pi.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            resp['pi'] = piSer.data

            if pi.manual_control:
                ctrlUpdate = ControllerUpdate.objects.filter(device__pi__pk=pk, executed=False)
                try:
                    ctrlUpdateSer = ControllerUpdateSerializer(ctrlUpdate, many=True)
                except ControllerUpdate.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                if ctrlUpdate:
                    resp['controllerUpdates'] = ctrlUpdateSer.data
            else:
                ControllerUpdate.objects.filter(device__pi__pk=pk, executed=False).update(executed=True)

            return Response(resp, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class testAPI(APIView):

    def get(self, request, pk):
        resp = {}
        pi = get_object_or_404(Pi, pk=pk)
        endInstance = pi.get_end_instance()
        activeInstance = pi.get_active_instance()
        startInstance = pi.get_start_instance()
        try:
            endInstanceSer = ExperimentInstanceSerializer(endInstance, many=True)
            activeInstanceSer = ExperimentInstanceSerializer(activeInstance, many=True)
            startInstanceSer = ExperimentInstanceSerializer(startInstance, many=True)
        except ExperimentInstance.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if endInstance:
            resp['endInstance'] = endInstanceSer.data
        if activeInstance:
            resp['activeInstance'] = activeInstanceSer.data
        if startInstance:
            resp['startInstance'] = startInstanceSer.data

        if pi.manual_control and startInstance:
            pi.manual_control = False
            pi.save()
        elif (not pi.manual_control) and (not startInstance) and endInstance:
            pi.manual_control = True
            pi.save()

        try:
            piSer = PiSerializer(pi)
        except Pi.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        resp['pi'] = piSer.data

        if pi.manual_control:
            ctrlUpdate = ControllerUpdate.objects.filter(device__pi__pk=pk, executed=False)
            try:
                ctrlUpdateSer = ControllerUpdateSerializer(ctrlUpdate, many=True)
            except ControllerUpdate.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if ctrlUpdate:
                resp['controllerUpdates'] = ctrlUpdateSer.data
        else:
            ControllerUpdate.objects.filter(device__pi__pk=pk, executed=False).update(executed=True)

        return Response(resp, status=status.HTTP_200_OK)
