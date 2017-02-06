from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success

from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .models import *
from .forms import *

class PiList(View):
    
    @method_decorator(login_required)
    def get(self, request, parent_template=None):
        if request.user.is_staff:
            pis = Pi.objects.all()
        else:
            pis = Pi.objects.filter(user = request.user)
        return render(
            request,
            'foodcomputer/pi_list.html',
            {'pis': pis,
             'parent_template': parent_template})


class PiCreate(ObjectCreateMixin, View):
    form_class = PiForm
    template_name = 'foodcomputer/create_form.html'
    form_url = reverse_lazy('foodcomputer:pi_create')
    parent_template=None
    model_name = 'Pi'


class PiUpdate(ObjectUpdateMixin, View):
    form_class = PiForm
    model = Pi
    template_name = 'foodcomputer/update_form.html'
    parent_template=None


class PiDelete(ObjectDeleteMixin, View):
    model = Pi
    success_url = reverse_lazy('foodcomputer:piList')
    template_name = 'foodcomputer/delete_confirm.html'
    parent_template=None