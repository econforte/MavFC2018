from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages import success
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden


def get_create_bcs(model_name):
    bc = []
    bc.append(('active', 'Create '+model_name))
    bc.append((reverse('experiment:experiment_list'), 'Experiment List'))
    bc.append(('/', 'Home'))
    return bc


class ObjectCreateMixin:
    form_class = None
    template_name = ''
    form_url = ''
    parent_template=None
    model_name = ''
    cancel_url = ''
    
    @method_decorator(login_required)
    def get(self, request):
        # if not request.user.is_staff: return HttpResponseForbidden()
        return render(
            request,
            self.template_name,
            {'form': self.form_class,
             'form_url': self.form_url,
             'cancel_url': self.cancel_url,
             'model_name': self.model_name,
             'breadcrumb_list': get_create_bcs(self.model_name),
             'parent_template': self.parent_template})
    
    @method_decorator(login_required)
    def post(self, request):
        # if not request.user.is_staff: return HttpResponseForbidden()
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            success(request, self.model_name+' was successfully added.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'form_url': self.form_url,
             'cancel_url': self.cancel_url,
             'model_name': self.model_name,
             'breadcrumb_list': get_create_bcs(self.model_name),
             'parent_template': self.parent_template})


class ObjectUpdateMixin:
    form_class = None
    model = None
    template_name = ''
    parent_template=None
    model_name=''
    cancel_url = ''
    
    @method_decorator(login_required)
    def get(self, request, pk):
        # if not request.user.is_staff: return HttpResponseForbidden()
        obj = get_object_or_404(self.model, pk=pk)
        return render(
            request,
            self.template_name,
            {'form': self.form_class(instance=obj),
             'obj': obj,
             'cancel_url': self.cancel_url,
             'model_name': self.model_name,
             'parent_template': self.parent_template})
    
    @method_decorator(login_required)
    def post(self, request, pk):
        # if not request.user.is_staff: return HttpResponseForbidden()
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            success(request, self.model_name+' was successfully updated.')
            return redirect(new_obj)
        return render(
            request,
            self.template_name,
            {'form': bound_form,
             'obj': obj,
             'cancel_url': self.cancel_url,
             'model_name': self.model.__name__,
             'parent_template': self.parent_template})


class ObjectDeleteMixin:
    model = None
    success_url = ''
    template_name = ''
    parent_template = None
    model_name = ''
    cancel_url = ''
    
    @method_decorator(login_required)
    def get(self, request, pk):
        # if not request.user.is_staff: return HttpResponseForbidden()
        obj = get_object_or_404(self.model, pk=pk)
        return render(
            request,
            self.template_name,
            {'obj': obj,
             'cancel_url': self.cancel_url,
             'model_name': self.model.__name__,
             'parent_template': self.parent_template})
    
    @method_decorator(login_required)
    def post(self, request, pk):
        # if not request.user.is_staff: return HttpResponseForbidden()
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        success(request, self.model_name+' was successfully deleted.')
        return HttpResponseRedirect(self.success_url)
        
        
        
        
        
        