from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q

from experiment.models import ExperimentInstance

from datetime import datetime


class Address(models.Model):
    name = models.CharField(max_length=100,)
    street_line_1 = models.CharField(max_length=75,)
    street_line_2 = models.CharField(max_length=75, blank=True, null=True,)
    city = models.CharField(max_length=30,)
    state = models.CharField(max_length=2,)
    zip = models.CharField(max_length=10,)

    def __str__(self):
        return "{p} {n}: {c}, {s}".format(p=self.pk, n=self.name, c=self.city, s=self.state)

    def get_absolute_url(self):
        return reverse('foodcomputer:address_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:address_create')

    def get_update_url(self):
        return reverse('foodcomputer:address_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:address_delete', kwargs={'pk': self.pk})

    def get_single_line_str(self):
        if self.street_line_2:
            return "{l1}, {l2}, {c}, {s} {z}".format(l1=self.street_line_1, l2=self.street_line_2, c=self.city, s=self.state, z=self.zip)
        else:
            return "{l1}, {c}, {s} {z}".format(l1=self.street_line_1, c=self.city, s=self.state, z=self.zip)

    def get_multi_line_str(self):
        return "{l1}\n{l2}\n{c}, {s} {z}".format(l1=self.street_line_1, l2=self.street_line_2, c=self.city, s=self.state, z=self.zip)


class Pi(models.Model):
    name = models.CharField(max_length=100,)
    pi_SN = models.CharField(max_length=50, verbose_name="Serial Number",)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    manual_control = models.BooleanField(default=False,)

    def __str__(self):
        return str(self.pk) +': '+self.name + ': ' + self.pi_SN

    def get_absolute_url(self):
        return reverse('foodcomputer:pi_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:pi_create')

    def get_update_url(self):
        return reverse('foodcomputer:pi_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:pi_delete', kwargs={'pk': self.pk})

    def get_list_url(self):
        return reverse('foodcomputer:pi_list')

    def get_active_instance(self):
        instance = ExperimentInstance.objects.filter(active=True, experiment__pi__pk=self.pk)
        if instance:
            return instance
        else:
            return None

    def get_current_instance(self):
        instance = ExperimentInstance.objects.filter(start__lte=datetime.now(), end__gt=datetime.now(), experiment__pi__pk=self.pk)
        if instance:
            return instance
        else:
            return None

    def get_start_instance(self):
        instance = ExperimentInstance.objects.filter(active=False, start__lte=datetime.now(), end__gt=datetime.now(), experiment__pi__pk=self.pk)
        if instance:
            return instance
        else:
            return None

    def get_end_instance(self):
        instance = ExperimentInstance.objects.filter(Q(active=True, experiment__pi__pk=self.pk) & (Q(start__gt=datetime.now()) | Q(end__lte=datetime.now())))
        if instance:
            return instance
        else:
            return None

    def get_device_num(self):
        return len(self.devices.all())

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == []:
            bc.append(('active', pre+self.name))
        else:
            bc.append((self.get_absolute_url, self.name))
        bc.append((self.get_list_url, 'Food Computer List'))
        bc.append(('/home/', 'Home'))
        return bc


class Device(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE, related_name="devices",)
    device_type = models.ForeignKey('DeviceType', on_delete=models.CASCADE, related_name="devices",)
    device_id = models.CharField(max_length=50, verbose_name="Device ID",)
    residual_threshold = models.FloatField()
    deactivated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)+ ": " + self.pi.name + ': ' + self.device_type.name + ': ' + self.device_id

    def get_device_name(self):
        return self.device_type.name + ': ' + self.device_id

    def get_absolute_url(self):
        return reverse('foodcomputer:device_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:device_create')

    def get_update_url(self):
        return reverse('foodcomputer:device_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:device_delete', kwargs={'pk': self.pk})

    def get_list_url(self):
        return self.pi.get_absolute_url()

    def get_threshold(self):
        return (self.residual_threshold + self.device_type.bio_threshold)

    def get_current_value(self):
        return self.data.latest('timestamp')

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def gen_breadcrumbs(self, bc=[]):
        if bc == []:
            bc.append(('active', self.device_type.name))
        else:
            bc.append((self.get_absolute_url, self.device_type.name))
        return self.pi.gen_breadcrumbs(bc)


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="data",)
    timestamp = models.DateTimeField()
    data_value = models.FloatField()
    is_anomaly = models.BooleanField()

    def __str__(self):
        return str(self.pk) + ' [' + str(self.timestamp) + ']: ' + str(self.data_value)

    def get_absolute_url(self):
        return reverse('foodcomputer:data_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:data_create')

    def get_update_url(self):
        return reverse('foodcomputer:data_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:data_delete', kwargs={'pk': self.pk})

    def get_list_url(self):
        return self.device.get_absolute_url()


class DeviceType(models.Model):
    name = models.CharField(max_length=100,)
    model_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Model ID",)
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, related_name="device_types",)
    data_type = models.ForeignKey('DataType', on_delete=models.CASCADE, related_name="device_types",)
    is_controller = models.BooleanField()
    bio_threshold = models.FloatField(verbose_name='Biological Threshold', default=0.0)

    def __str__(self):
        return str(self.pk)+ " " + self.name + ": " + self.unit_type.name

    def get_short_name(self):
        if len(self.name) > 20:
            return self.name[:20]+"..."
        else:
            return self.name

    def get_absolute_url(self):
        return reverse('foodcomputer:devicetype_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:devicetype_create')

    def get_update_url(self):
        return reverse('foodcomputer:devicetype_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:devicetype_delete', kwargs={'pk': self.pk})


class UnitType(models.Model):
    name = models.CharField(max_length=30,)
    abbr = models.CharField(max_length=10,)
    descr = models.TextField()
    ##### @elocke: moved the following from the DataType, per @scwest
    min_limit = models.FloatField(blank=True, null=True,)
    max_limit = models.FloatField(blank=True, null=True,)
    #####

    def __str__(self):
        return str(self.pk) + str(": ") + self.name

    def get_absolute_url(self):
        return reverse('foodcomputer:unittype_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:unittype_create')

    def get_update_url(self):
        return reverse('foodcomputer:unittype_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:unittype_delete', kwargs={'pk': self.pk})


class DataType(models.Model):
    name = models.CharField(max_length=30,)
    descr = models.TextField()
    ##### @elocke: move the following fields to UnitType, per @scwest
    # min_limit = models.FloatField(blank=True, null=True,)
    # max_limit = models.FloatField(blank=True, null=True,)
    #####

    def __str__(self):
        return str(self.pk) + str(": ") + self.name

    def get_absolute_url(self):
        return reverse('foodcomputer:pi_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('foodcomputer:pi_create')

    def get_update_url(self):
        return reverse('foodcomputer:pi_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foodcomputer:pi_delete', kwargs={'pk': self.pk})


class ControllerUpdate(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="Updates",)
    turn_on = models.BooleanField()
    timestamp = models.DateTimeField()
    executed =models.BooleanField()
