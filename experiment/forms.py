from django import forms
from foodcomputer.models import Device
# from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Experiment, ExperimentRule, ExperimentInstance, UserExperimentInstance
from foodcomputer.models import Device

import pytz
import datetime


tz = pytz.timezone('America/Chicago')


class ExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Experiment
        fields = '__all__'


class ExperimentRuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.pi_pk = kwargs.pop('pi_pk')
        self.isupdate = kwargs.pop('isupdate')
        super(ExperimentRuleForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['hour'].widget.attrs.update({
            'min':'0', 'max': '23', 'step':'1', 'placeholder':'Integers from 0 to 23'
        })
        self.fields['minute'].widget.attrs.update({
            'min':'0', 'max':'59', 'step':'1', 'placeholder':'Integers from 0 to 59'
        })
        self.fields['device'].queryset = Device.objects.filter(pi__pk = self.pi_pk)
        if self.isupdate:
            self.fields['device'].widget.attrs.update({'disabled':''})

    class Meta:
        model = ExperimentRule
        fields = ('device', 'hour', 'minute', 'baseline_target', 'days',)

    def clean_baseline_target(self):
        baseline_target = self.cleaned_data['baseline_target']
        devicePK = self.cleaned_data['device']
        dt = devicePK.device_type
        minl = None
        maxl = None
        if dt.unit_type.min_limit is not None and dt.data_type.min_limit is not None:
            minl = max([dt.unit_type.min_limit, dt.data_type.min_limit])
        elif dt.unit_type.min_limit is not None:
            minl = dt.unit_type.min_limit
        elif dt.data_type.min_limit is not None:
            minl = dt.data_type.min_limit
        if dt.unit_type.max_limit is not None and dt.data_type.max_limit is not None:
            maxl = min([dt.unit_type.max_limit, dt.data_type.max_limit])
        elif dt.unit_type.max_limit is not None:
            maxl = dt.unit_type.max_limit
        elif dt.data_type.max_limit is not None:
            maxl = dt.data_type.max_limit
        if minl is not None:
            if baseline_target < minl:
                raise forms.ValidationError('The baseline target can not be lower than ' + str(minl) + ', for the ' + str(dt.name) + ' device.')
        if maxl is not None:
            if baseline_target > maxl:
                raise forms.ValidationError('The baseline target can not be greater than ' + str(maxl) + ', for the ' + str(dt.name) + ' device.')
        return baseline_target


class ExperimentRuleUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.device_pk = kwargs.pop('device_pk')
        super(ExperimentRuleUpdateForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['hour'].widget.attrs.update({
            'min':'0', 'max': '23', 'step':'1', 'placeholder':'Integers from 0 to 23'
        })
        self.fields['minute'].widget.attrs.update({
            'min':'0', 'max':'59', 'step':'1', 'placeholder':'Integers from 0 to 59'
        })

    class Meta:
        model = ExperimentRule
        fields = ('hour', 'minute', 'baseline_target', 'days',)

    def clean_baseline_target(self):
        baseline_target = self.cleaned_data['baseline_target']
        dt = Device.objects.get(pk=self.device_pk).device_type
        minl = False
        maxl = False
        if dt.unit_type.min_limit is not None and dt.data_type.min_limit is not None:
            minl = max([dt.unit_type.min_limit, dt.data_type.min_limit])
        elif dt.unit_type.min_limit is not None:
            minl = dt.unit_type.min_limit
        elif dt.data_type.min_limit is not None:
            minl = dt.data_type.min_limit
        if dt.unit_type.max_limit is not None and dt.data_type.max_limit is not None:
            maxl = min([dt.unit_type.max_limit, dt.data_type.max_limit])
        elif dt.unit_type.max_limit is not None:
            maxl = dt.unit_type.max_limit
        elif dt.data_type.max_limit is not None:
            maxl = dt.data_type.max_limit
        if minl is not None:
            if baseline_target < minl:
                raise forms.ValidationError('The baseline target can not be lower than ' + str(minl) + ', for the ' + str(dt.name) + ' device.')
        if maxl is not None:
            if baseline_target > maxl:
                raise forms.ValidationError('The baseline target can not be greater than ' + str(maxl) + ', for the ' + str(dt.name) + ' device.')
        return baseline_target


class ExperimentInstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentInstanceForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget=forms.DateTimeInput(attrs={'type':'datetime-local'}, format='%Y-%m-%dT%H:%M')
        self.fields['start'].input_formats=('%Y-%m-%dT%H:%M',)
        self.fields['end'].widget=forms.DateTimeInput(attrs={'type':'datetime-local'}, format='%Y-%m-%dT%H:%M')
        self.fields['end'].input_formats=('%Y-%m-%dT%H:%M',)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ExperimentInstance
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ExperimentInstanceForm, self).clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start and end:
            if start >= end:
                raise forms.ValidationError("The start occurs after or equal to the end.")
            exp = cleaned_data.get("experiment")
            instances = ExperimentInstance.objects.filter(experiment__pi__pk=exp.pi.pk).exclude(id=self.instance.pk)
            for instance in instances:
                if end >= instance.start and end < instance.end:
                    raise forms.ValidationError("The end occurs within another instance scheduled for this pi.")
                if start >= instance.start and start < instance.end:
                    raise forms.ValidationError("The start occurs within another instance scheduled for this pi.")
                if instance.start >= start and instance.end < end:
                    raise forms.ValidationError("Another instance scheduled during this time period for this pi.")


class ExperimentInstanceAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.experiment_pk = kwargs.pop('experiment_pk')
        super(ExperimentInstanceAddForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget=forms.DateTimeInput(attrs={'type':'datetime-local'}, format='%Y-%m-%dT%H:%M')
        self.fields['start'].input_formats=('%Y-%m-%dT%H:%M',)
        self.fields['end'].widget=forms.DateTimeInput(attrs={'type':'datetime-local'}, format='%Y-%m-%dT%H:%M')
        self.fields['end'].input_formats=('%Y-%m-%dT%H:%M',)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = ExperimentInstance
        fields = ('start', 'end', )

    def clean(self):
        cleaned_data = super(ExperimentInstanceAddForm, self).clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start and end:
            if start >= end:
                raise forms.ValidationError("The start occurs after or equal to the end.")
            exp = Experiment.objects.get(pk=self.experiment_pk)
            instances = ExperimentInstance.objects.filter(experiment__pi__pk=exp.pi.pk)
            for instance in instances:
                if end >= instance.start and end < instance.end:
                    raise forms.ValidationError("The end occurs within another instance scheduled for this pi.")
                if start >= instance.start and start < instance.end:
                    raise forms.ValidationError("The start occurs within another instance scheduled for this pi.")
                if instance.start >= start and instance.end < end:
                    raise forms.ValidationError("Another instance scheduled during this time period for this pi.")

    def clean_start(self):
        start = self.cleaned_data['start']
        if start.replace(tzinfo=None) < (datetime.datetime.now(tz=tz) - datetime.timedelta(hours=1)).replace(tzinfo=None):
            raise forms.ValidationError('The start ('+str((start))+') can not be in the past.')
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        if end.replace(tzinfo=None) < (datetime.datetime.now(tz=tz) - datetime.timedelta(hours=1)).replace(tzinfo=None):
            raise forms.ValidationError('The end ('+str(end)+') can not be in the past.')
        return end


class UserExperimentInstanceAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent')
        super(UserExperimentInstanceAddForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['user'].queryset = User.objects.exclude(experiment_instances__experiment_instance__in=[self.parent])

    class Meta:
        model = UserExperimentInstance
        fields = ['user', 'is_user']


class UserExperimentInstanceForm(forms.ModelForm):

    class Meta:
        model = UserExperimentInstance
        fields = ['is_user']
