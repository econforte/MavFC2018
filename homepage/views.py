from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from datetime import datetime, timedelta, tzinfo
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success
from django.http import HttpResponse

from foodcomputer.models import *
from experiment.models import *


import pytz


# def home(request):
#     # return HttpResponse("<h2>Hey!</h2>");
#     return render(request, 'homepage/Justpage.html')


class Homepage(View):

    #@method_decorator(login_required)
    def get(self, request, parent_template=None):
        tz = pytz.timezone('America/Chicago')
        if request.user.is_authenticated():
            if request.user.is_staff:
                pis = Pi.objects.all()
                experiments = Experiment.objects.all()
                dcPis = Pi.objects.exclude(devices__data__timestamp__gt=datetime.now(tz=tz).replace(tzinfo=None) - timedelta(minutes=60))
            else:
                pis = Pi.objects.filter(Q(user=request.user) | Q(experiment__instances__active=True, experiment__instances__instance_users__user__in=[request.user]))
                experiments = Experiment.objects.filter(Q(pi__user__pk=request.user.pk) | Q(instances__instance_users__user__pk=request.user.pk))
                dcPis = Pi.objects.exclude(devices__data__timestamp__gt=datetime.now(tz=tz).replace(tzinfo=None) - timedelta(minutes=60))\
                    .filter(Q(user=request.user) | Q(experiment__instances__active=True, experiment__instances__instance_users__user__in=[request.user]))
            return render(
                request,
                'homepage/dashboard.html',
                {'pis': pis,
                 'experiments': experiments,
                 'dcPis': dcPis,
                 'parent_template': parent_template})
        else:
            return render(request, 'homepage/Justpage.html', {'parent_template': parent_template})

