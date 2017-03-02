from django import forms
# from django.core.exceptions import ValidationError

from .models import Experiment, ExperimentRule


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
        super(ExperimentRuleForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ExperimentRule
        fields = '__all__'