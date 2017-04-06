from django import forms
from foodcomputer.models import Device
# from django.core.exceptions import ValidationError

from .models import Experiment, ExperimentRule, ExperimentInstance, UserExperimentInstance


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
        super(ExperimentInstanceAddForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ExperimentInstance
        exclude = ('pi',)


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
