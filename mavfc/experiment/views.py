from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success

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