from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.contrib.messages import success

# Imports used to serve JSON
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions

from .serializers import *
from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *

import time

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
        return render(
            request,
            self.template_name,
            {'obj': obj,
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


class DeviceDetail(View):
    model = Device
    model_name = 'Device'
    template_name = 'foodcomputer/device_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(
            request,
            self.template_name,
            {'device': obj,
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



#
# def deviceCurrentValue(request, pk):
#     curVal = Data.objects.filter(device__pk=pk).latest('timestamp')
#     serializer = dataSerializer(curVal, many=False)
#     return JSONResponse(serializer.data)


@csrf_exempt
def addressListJSON(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def addressJSON(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(address, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        address.delete()
        return HttpResponse(status=204)

class todoCheckJSON(APIView):
    #getTodoList Implementation
    #long polling idea
    def get(request, pk):
        for i in range(60):
            if something_happened():
                return http.HttpResponse()
            time.sleep(1)
        return http.HttpResponse()

class keyJSON(APIView):
    #getFoodComputerKey Implementation
    def get(request, pk):
        return HttpResponse(status=200)
        # return HttpResponse(Pi.objects.get(pk=pk), status=200)


class commandsJSON(APIView):
    #getFoodComputerCommands Implementation
    def get(request, pk):
        return HttpResponse(status=200)

class sensorValues(APIView):

    def put(self, request, pk):
        sensorVals = get_object_or_404(Data, pk=pk)
        # try:
        #     sensorVals = Data.objects.get(pk=pk)
        # except Data.DoesNotExist:
        #     return HttpResponse(status=404)
        data = JSONParser().parse(request)
        serializer = dataSerializer(sensors, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    def get(self, request, pk):
        try:
            sensorVals = Data.objects.get(pk=pk)
        except Data.DoesNotExist:
            return HttpResponse(status=404)
        serializer = dataSerializer(sensorVals)
        # return JSONResponse(serializer.data)
        return Response(serializer.data)

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
        serializer = dataSerializer(data=request.data, many=True)  # removed unneeded sensorVals var
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
