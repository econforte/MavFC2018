from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success

from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *
import collections

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