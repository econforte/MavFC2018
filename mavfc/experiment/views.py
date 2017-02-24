from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success

from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *


class ExperimentList(View):
    @method_decorator(login_required)
    def get(self, request, parent_template=None):
        if request.user.is_staff:
            experiments = Experiment.objects.all()
        else:
            experiments = Experiment.objects.all()
        return render(
            request,
            'experiment/experiment_list.html',
            {'experiments': experiments,
             'parent_template': parent_template})


class ExperimentDetail(View):
    model = Experiment
    model_name = 'Experiment'
    template_name = 'experiment/experiment_detail.html'
    parent_template = None

    @method_decorator(login_required)
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(
            request,
            self.template_name,
            {'obj': obj,
             'model_name': self.model_name,
             'parent_template': self.parent_template})

# class ExperimentCreate(ObjectCreateMixin, View):
#     form_class = ExperimentForm
#     template_name = 'experiment/create_page.html'
#     form_url = reverse_lazy('experiment:experiment_create')
#     parent_template=None
#     model_name = 'Experiment'
#
#
# class ExperimentUpdate(ObjectUpdateMixin, View):
#     form_class = ExperimentForm
#     model = Experiment
#     template_name = 'experiment/update_page.html'
#     parent_template=None
#
#
class ExperimentDelete(ObjectDeleteMixin, View):
    model = Experiment
    success_url = reverse_lazy('experiment:experimentList')
    template_name = 'experiment/delete_confirm.html'
    parent_template=None
