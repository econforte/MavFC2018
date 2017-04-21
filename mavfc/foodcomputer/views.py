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
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# Imports used to serve JSON
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from experiment.serializers import ExperimentInstanceSerializer
from experiment.models import ExperimentInstance
from .serializers import *
from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .utils import ChartDataPreparation, DownloadDataPreparation, DeviceDataPreparation
from .models import *
from .forms import *
import datetime
import csv

class PiList(View):

    @method_decorator(login_required)
    def get(self, request, parent_template=None):
        if request.user.is_staff:
            pis = Pi.objects.all()
        else:
            pis = Pi.objects.filter(Q(user=request.user) | Q(experiment__instances__active=True, experiment__instances__instance_users__user__in=[request.user]))
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
        obj = None
        if request.user.is_staff or request.user.pis.filter(pk=pk) or request.user.experiment_instances.filter(experiment__pi__pk=pk):
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
             'parent_template': self.parent_template,
             'show_anomalies':        False})


class PiChart(View):
    model = Pi
    model_name = 'Food Computer Chart'
    template_name = 'foodcomputer/pi_data_page.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        if request.user.is_staff or request.user.pis.filter(pk=pk) or request.user.experiment_instances.filter(experiment__pi__pk=pk):
            obj = get_object_or_404(self.model, pk=pk)
        else:
            return HttpResponseForbidden()
        form_class = AdvancedOptionsForm(request=request, pk=pk)

        cdp = ChartDataPreparation()
        namelist = cdp.getNameList(obj)
        isActuator = cdp.getActuatorDictionary(obj)
        time2sensor = cdp.initializeDataValues(obj)
        downloadable_table = cdp.constructTable(time2sensor, namelist, isActuator, sep='\\n') #####
        time2sensor = cdp.subsetDataValues(time2sensor, 500)
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
                       'parent_template':       self.parent_template,\
                       'download_table':        downloadable_table,
                       'show_anomalies':        False})

    def post(self, request, pk):
        if not (request.user.is_staff or request.user.pis.filter(pk=pk) or request.user.experiment_instances.filter(experiment__pi__pk=pk)):
            return HttpResponseForbidden()
        obj = get_object_or_404(self.model, pk=pk)
        form_class = AdvancedOptionsForm(request.POST, request=request, pk=pk)
        cdp = ChartDataPreparation()
        height = '900px'

        if form_class.is_valid():
            cdp = ChartDataPreparation(start_date=datetime.datetime.strptime(form_class.cleaned_data['start_date'], '%Y-%m-%dT%H:%M'),\
                                       end_date=datetime.datetime.strptime(form_class.cleaned_data['end_date'], '%Y-%m-%dT%H:%M'),\
                                       show_anomalies=form_class.cleaned_data['show_anomalies'],
                                       sensors=form_class.cleaned_data['devices'],
                                       experiment=form_class.cleaned_data['experiments'])

        namelist = cdp.getNameList(obj)
        isActuator = cdp.getActuatorDictionary(obj)
        if not 0 in [isActuator[x] for x in isActuator if x in namelist]:
            height = str(60+len(namelist)*12)+"px"
        time2sensor = cdp.initializeDataValues(obj)
        downloadable_table = cdp.constructTable(time2sensor, namelist, isActuator, sep='\\n') #####
        time2sensor = cdp.subsetDataValues(time2sensor, 500, form_class.cleaned_data['show_anomalies'])
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
                       'parent_template':       self.parent_template,\
                       'download_table':        downloadable_table,\
                       'show_anomalies':        form_class.cleaned_data['show_anomalies']})




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
        if not (request.user.is_staff or request.user.pis.filter(pk=pk) or request.user.experiment_instances.filter(experiment__pi__pk=pk)):
            return HttpResponseForbidden()
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
        if not (request.user.is_staff or request.user.pis.filter(pk=obj.pi.pk) or request.user.experiment_instances.filter(experiment__pi__pk=obj.pi.pk)):
            return HttpResponseForbidden()

        ddp = DeviceDataPreparation(obj)
        time2sensor = ddp.initializeDeviceDataValues(obj)
        time2sensor = ddp.subsetDataValues(time2sensor)
        prestring = ddp.constructTable(time2sensor, numdp=200)

        height = "700px"
        if obj.device_type.is_controller:
            height = "200xp"

        return render(
            request,
            self.template_name,
            {'device': obj,
             'prestring': prestring,
             'height': height,
             'model_name': self.model_name,
             'parent_template': self.parent_template,
             'show_anomalies': False})


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
        if not (request.user.is_staff or request.user.pis.filter(pk=device.pi.pk) or request.user.experiment_instances.filter(experiment__pi__pk=device.pi.pk)):
            return HttpResponseForbidden()
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


class DeviceCtrlAPI(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ControllerUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PiCurrentValueAPI(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        # Not sure if this db call is correct/may not need timestamp
        curVal = get_object_or_404(Pi, pk=pk)
        jsonObj = PiManualCtrlSerializer(curVal, many=False)
        return Response(jsonObj.data)

    def put(self, request, pk, format=None):
        curVal = get_object_or_404(Pi, pk=pk)
        serializer = PiManualCtrlSerializer(curVal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressAdd(View):
    parent = Pi
    form_class = AddressForm
    template_name = 'foodcomputer/create_page.html'
    parent_template = None
    model_name = 'Address'

    @method_decorator(login_required)
    def get(self, request, pk):
        if not (request.user.is_staff or request.user.pis.filter(pk=pk)):
            return HttpResponseForbidden()
        pi = get_object_or_404(Pi, pk=pk)
        return render(
            request,
            self.template_name,
            {'form': self.form_class,
             'form_url': reverse('foodcomputer:address_add', kwargs={'pk': pk}),
             'cancel_url': reverse('foodcomputer:pi_detail', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'breadcrumb_list': pi.get_add_address_breadcrumbs(),
             'parent_template': self.parent_template})

    @method_decorator(login_required)
    def post(self, request, pk):
        if not (request.user.is_staff or request.user.pis.filter(pk=pk)):
            return HttpResponseForbidden()
        pi = get_object_or_404(Pi, pk=pk)
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            pi.address = new_obj
            pi.save()
            success(request, self.model_name + ' was successfully added.')
            return redirect(pi)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'form_url': reverse('foodcomputer:address_add', kwargs={'pk': pk}),
             'cancel_url': reverse('foodcomputer:pi_detail', kwargs={'pk': pk}),
             'model_name': self.model_name,
             'breadcrumb_list': pi.get_add_address_breadcrumbs(),
             'parent_template': self.parent_template})


class AddressUpdate(ObjectUpdateMixin, View):
    model = Address
    form_class = AddressForm
    template_name = 'foodcomputer/update_page.html'
    parent_template = None
    model_name = 'Address'


class AddressDelete(ObjectDeleteMixin, View):
    model = Address
    success_url = reverse_lazy('foodcomputer:pi_list')
    template_name = 'foodcomputer/delete_confirm.html'
    parent_template = None
    model_name = 'Address'


#----------Pi Send-------------


class initPi(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Post JSON Structure
        #       {
        #           "name": "FoodComputer1",
        #           "pi_SN": "1234567890",
        #           "manual_control": true
        #       }
        serializer = PiSerializer(data=request.data)
        if serializer.is_valid():
            pi = serializer.save()
            user = User.objects.create_user('FC'+pi.pi_SN, password='tempPW'+pi.pi_SN)
            token = Token.objects.get_or_create(user=user)
            user.set_password(token[0].key)
            user.save()
            return Response({"pi":serializer.data, "token":token[0].key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class initDevices(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            devicetypes = DeviceType.objects.all()
            serializer = deviceTypesSerializer(devicetypes, many=True)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

class anomalyEmail(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Post JSON Structure
        #   {
        #       "pi": 1,
        #       "level": 1,
        #       "message": "It was Sean and his team of dolphins."
        #   }
        serializer = emailSerializer(data=request.data)
        if serializer.is_valid():
            sent = serializer.send_mail();
            if sent:
                return Response("Email(s) Sent")
        else: return Response("No Email(s) Sent")


#----------Server Push-------------

class ServerPushAPI(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Server Push
    # Long polling idea
    def post(self, request, pk):
        serializer = PiStateSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.updateDB()
            data = request.data
            if str(data['pi']['pk']) == pk:
                pi = get_object_or_404(Pi, pk=pk)
            else:
                return Response({'Error':"PK doesn't match"}, status=status.HTTP_400_BAD_REQUEST)
            if data['pi']['pi_SN'] != pi.pi_SN:
                return Response({'Error': "Serial number doesn't match"}, status=status.HTTP_400_BAD_REQUEST)
            if 'lastControllerUpdateTime' in data:
                last = data['lastControllerUpdateTime']
                ControllerUpdate.objects.filter(device__pi__pk=pi.pk, executed=False, timestamp__lte=last).update(executed=True)

            if 'activeInstance' in data:
                activeInstance = data['activeInstance']
                newActInst = ExperimentInstance.objects.get(pk=activeInstance)
                if not newActInst.active:
                    actInst = pi.get_active_instance()[0]
                    actInst.active = False
                    actInst.save()
                    newActInst.active = True
                    newActInst.save()
            # Generate Push Response
            resp = {}
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
