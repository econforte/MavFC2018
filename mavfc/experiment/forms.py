from django import forms
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
        super(ExperimentRuleForm, self).__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ExperimentRule
        fields = '__all__'


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
