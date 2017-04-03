from django import forms
# from django.core.exceptions import ValidationError

from .models import Pi, Device


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
    start_date = forms.DateField(input_formats="%Y-%m-%d %H:%M:%S", widget=forms.SelectDateWidget())
    end_date = forms.DateField(input_formats="%Y-%m-%d %H:%M:%S", widget=forms.SelectDateWidget())
    show_anomalies = forms.BooleanField()
    devices = forms.MultipleChoiceField()
    
    #def __init__(self, *args, **kwargs):
        #self.pi_pk = kwargs.pop('pi_pk')
        #super(AdvancedOptions, self).__init__(*args, **kwargs)
        #self.fields['devices'].queryset = Device.objects.filter(pi__pk=self.pi_pk)
#     class Meta:
#         model = Pi
#         fields = ['start_date', 'end_date', 'show_anomalies']#, 'sensors']