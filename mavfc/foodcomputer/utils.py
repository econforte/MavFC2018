from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success, error

from .models import Data, Device
import collections
import math
from datetime import datetime


class ObjectCreateMixin:
    form_class = None
    template_name = ''
    form_url = ''
    parent_template=None
    model_name = ''
    cancel_url = ''
    
    @method_decorator(login_required)
    def get(self, request):
        return render(
            request,
            self.template_name,
            {'form': self.form_class,
             'form_url': self.form_url,
             'cancel_url': self.cancel_url,
             'model_name': self.model_name,
             'parent_template': self.parent_template})
    
    @method_decorator(login_required)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            success(request, self.model_name+' was successfully added.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'model_name': self.model_name,
             'parent_template': self.parent_template})


class ObjectUpdateMixin:
    form_class = None
    model = None
    template_name = ''
    parent_template=None
    
    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(
            request,
            self.template_name,
            {'form': self.form_class(instance=obj),
             'obj': obj,
             'model_name': self.model.__name__,
             'parent_template': self.parent_template})
    
    @method_decorator(login_required)
    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            success(request, self.model_name+' was successfully updated.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'obj': obj,
             'model_name': self.model.__name__,
             'parent_template': self.parent_template})


class ObjectDeleteMixin:
    model = None
    success_url = ''
    template_name = ''
    parent_template=None
    
    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(
            request,
            self.template_name,
            {'obj': obj,
             'model_name': self.model.__name__,
             'parent_template': self.parent_template})
    
    @method_decorator(login_required)
    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        success(request, self.model_name+' was successfully deleted.')
        return HttpResponseRedirect(self.success_url)
        

class DeviceDataPreparation():
    def __init__(self, obj):
        self.device_name = self.deviceName(obj)
        self.is_actuator = self.isController(obj)
    
    def deviceName(self, obj):
        return obj.device_type.name
    
    def isController(self, obj):
        return obj.device_type.is_controller
    
    def initializeDeviceDataValues(self, obj):
        time2sensor = {}
        for value in obj.data.all():
            dataValue = value.data_value
            if dataValue < 0:
                dataValue = 'NA'
            else:
                dataValue = str(dataValue)
            time2sensor[str(value.timestamp)] = dataValue
        return time2sensor
    
    def subsetDataValues(self, time2sensor, numdp=200):
        times = sorted([x for x in time2sensor])
        ss = len(times)/numdp # static shift
        spots = [math.floor(ss*x) for x in range(numdp)]
        time3sensor = collections.defaultdict(dict)
        if len(set(spots)) == 1: return time3sensor
        for spot in set(spots):
            time3sensor[times[spot]] = time2sensor[times[spot]]
        return time3sensor            
    
    def constructTable(self, time2sensor, numdp = 200):
        prestring = "date," + self.device_name + '\n'
        if self.is_actuator:
            prestring += "0,1\n"
        else:
            prestring += "0,0\n"
            
        for time in sorted([x for x in time2sensor]):
            prestring += str(time).split('+')[0] + ',' + str(time2sensor[time]) + '\n'
        return prestring
    
    

        
class ChartDataPreparation():
    def __init__(self, start_date=datetime.min, end_date=datetime.now(), experiment=None, show_anomalies=False, sensors=None):
        self.start_date = start_date
        self.end_date = end_date
        self.experiment = experiment
        self.show_anomalies = show_anomalies
        self.sensors = sensors
        return
    
    def getDates(self, experiment):
        self.start_date=None
        self.end_date=None  
        return
    
    def getActuatorDictionary(self, obj):
        isActuator = {}
        for device in obj.devices.all():
            if device.device_type.is_controller:
                isActuator[device.device_type.name] = 1
            else:
                isActuator[device.device_type.name] = 0
        return isActuator
    
    def initializeDataValues(self, obj):
        time2sensor = collections.defaultdict(dict)
        if self.sensors:            
            for device in self.sensors:
                for value in Data.objects.filter(device=device, timestamp__gte=self.start_date, timestamp__lte=self.end_date):
                    dataValue = value.data_value
                    if float(dataValue) < 0:
                        if self.show_anomalies:
                            dataValue = 'NAN'
                        else:
                            dataValue = 'NA'
                    time2sensor[str(value.timestamp)][device.device_type.name] = str(dataValue)
        else:
            for device in obj.devices.all():
                for value in Data.objects.filter(device=device, timestamp__gte=self.start_date, timestamp__lte=self.end_date):
                    dataValue = value.data_value
                    if float(dataValue) < 0:
                        if self.show_anomalies:
                            dataValue = 'NAN'
                        else:
                            dataValue = 'NA'
                    time2sensor[str(value.timestamp)][device.device_type.name] = str(dataValue)
            
        return time2sensor
        
    def subsetDataValues(self, time2sensor, numdp=200):
        times = sorted([x for x in time2sensor])
        ss = len(times)/numdp # static shift
        spots = [math.floor(ss*x) for x in range(numdp)]
        time3sensor = collections.defaultdict(dict)
        if len(set(spots)) == 1: return time3sensor
        for spot in set(spots):
            time3sensor[times[spot]] = time2sensor[times[spot]]
        return time3sensor
    
    def constructTable(self, time2sensor, namelist, isActuator):
        prestring = "date," + ','.join(namelist) + '\n' + ','.join(["0"]+[str(isActuator[x]) for x in namelist]) + '\n'
        for t in time2sensor:
            temp = [t.split('+')[0]]
            for name in namelist:
                if name in time2sensor[t]:
                    temp.append(str(time2sensor[t][name]))
                else:
                    temp.append('NA')
            prestring += ','.join(temp) + '\n'
        return prestring
    
    def getNameList(self, obj):
        device_names = obj.devices.all()
        if self.sensors:
            device_names = self.sensors
        return [device.device_type.name for device in device_names]
        
        
class DownloadDataPreparation():
    def __init__(self, pi):
        self.cdp = ChartDataPreparation()
        self.namelist = self.cdp.getNameList(pi) 
        
    def firstline(self, pi):
        return ['date'] + self.namelist
    
    def secondline(self, pi):
        isActuator = self.cdp.getActuatorDictionary(pi)
        return ['0'] + [isActuator[x] for x in self.namelist]
    
    def initializeDataValues(self, pi):
        return self.cdp.initializeDataValues(pi)
    
    def downloadFileGenerator(self, time2sensor):
        for time in sorted([x for x in time2sensor]):
            temp = [time.split('+')[0]]
            for name in self.namelist:
                if name in time2sensor[time]:
                    temp.append(time2sensor[time][name])
                else:
                    temp.append('NA')
            yield temp
            
        
    
        
        
        