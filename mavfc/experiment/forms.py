from django import forms
from foodcomputer.models import Device
# from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from django.utils import timezone

from .models import Experiment, ExperimentRule, ExperimentInstance, UserExperimentInstance


import datetime


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
            self.fields['device'].widget.attrs.update({
                'disabled':''
            })

    class Meta:
        model = ExperimentRule
        fields = ('device', 'hour', 'minute', 'baseline_target', 'days',)


class ExperimentInstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperimentInstanceForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ExperimentInstance
        fields = '__all__'


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
        if start < (timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - datetime.timedelta(hours=1)):
            raise forms.ValidationError('The start ('+str(start)+') can not be in the past.'+str(timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()) - datetime.timedelta(hours=1)))
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        if end < (timezone.now() - datetime.timedelta(hours=1)):
            raise forms.ValidationError('The end ('+str(end)+') can not be in the past.'+str(timezone.now() - datetime.timedelta(hours=1)))
        return end


class  UserExperimentInstanceAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserExperimentInstanceAddForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserExperimentInstance
        fields = ['user', 'is_user']
        #fields = forms.ModelChoiceField(queuryset = ..., empty_label= "(Nothing)" )
