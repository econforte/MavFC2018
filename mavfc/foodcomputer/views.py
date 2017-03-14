from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success
from django.http import HttpResponse

from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *

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