from django import forms
# from django.core.exceptions import ValidationError

from .models import Pi, Device
from django.forms.widgets import CheckboxSelectMultiple, DateInput,\
    SelectDateWidget, TimeInput
import datetime
from django.contrib.admin.widgets import AdminDateWidget


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
    start_date = forms.DateField(required=False,\
                                 label="Start Date",\
                                 widget=SelectDateWidget(years=range(2015, datetime.date.today().year)))
    start_time = forms.TimeField(required=False,\
                                 label="Start Time",\
                                 widget=forms.TimeInput(format='%H:%M:%S'))
    
    end_date = forms.SplitDateTimeField(required=False,\
                                        label="End Date",\
                                        widget=SelectDateWidget(years=range(2015, datetime.date.today().year)))
    end_time = forms.TimeField(required=False,\
                               label="End Time",\
                               widget=forms.TimeInput(format='%H:%M:%S'))
    
    show_anomalies = forms.BooleanField(label='Show Anomalies')
    devices = forms.ModelMultipleChoiceField(required=False,\
                                        label='Available Sensors and Actuators',\
                                        queryset=Device.objects.all(),\
                                        widget=CheckboxSelectMultiple())
        
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.pk = kwargs.pop('pk')
        self.user = request.user
        super(AdvancedOptionsForm, self).__init__(*args, **kwargs)
        
        

    
    #def __init__(self, *args, **kwargs):
        #self.pi_pk = kwargs.pop('pi_pk')
        #super(AdvancedOptions, self).__init__(*args, **kwargs)
        #self.fields['devices'].queryset = Device.objects.filter(pi__pk=self.pi_pk)
#     class Meta:
#         model = Pi
#         fields = ['start_date', 'end_date', 'show_anomalies']#, 'sensors']