from django import forms
# from django.core.exceptions import ValidationError

from .models import Pi, Device
from experiment.models import ExperimentInstance
from django.forms.widgets import CheckboxSelectMultiple, DateInput,\
    SelectDateWidget, TimeInput
import datetime


class PiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PiForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Pi
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Device
        fields = '__all__'
        
class AdvancedOptionsForm(forms.Form):
    start_date = forms.CharField(required=False, label="Start Date",\
                                 widget=forms.DateTimeInput(attrs={'type':'datetime-local', 'class':'form-control'}),\
                                 initial=datetime.datetime.strftime(datetime.datetime.min, '%Y-%m-%dT%H:%M'))
    end_date = forms.CharField(required=False, label="End Date",\
                                 widget=forms.DateTimeInput(attrs={'type':'datetime-local', 'class':'form-control'}),\
                                 initial=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M'))
    experiments = forms.ModelChoiceField(required=False, label="Experiments", queryset=ExperimentInstance.objects.all())
    show_anomalies = forms.BooleanField(required=False, label='Show Anomalies')
    devices = forms.ModelMultipleChoiceField(required=False, label='Sensors and Actuators',\
                                             queryset=Device.objects.all())#,\
                                             # widget=CheckboxSelectMultiple())
        
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.pk = kwargs.pop('pk')
        self.user = request.user
        super(AdvancedOptionsForm, self).__init__(*args, **kwargs)
        self.fields['experiments'].queryset = ExperimentInstance.objects.filter(experiment__pi__pk=self.pk)
        self.fields['experiments'].widget.attrs['class'] = 'form-control'
        self.fields['devices'].widget.attrs['class'] = 'form-control'
        self.fields['devices'].widget.attrs['size'] = '15'