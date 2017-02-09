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