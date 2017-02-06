from django import forms
# from django.core.exceptions import ValidationError

from .models import Pi

    

class PiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PiForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Pi
        fields = '__all__'