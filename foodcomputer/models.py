from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q

from experiment.models import ExperimentInstance

from datetime import datetime, timedelta

import pytz


tz = pytz.timezone('America/Chicago')


def parse_day_of_week(day):
    days_of_week = {'Monday':    0, 'monday':    0, 'Mon': 0, 'mon': 0, 'Mo': 0, 'mo': 0, 'M': 0, 'm': 0,
                    'Tuesday':   1, 'tuesday':   1, 'Tue': 1, 'tue': 1, 'Tu': 1, 'tu': 1, 'T': 1, 't': 1,
                    'Wednesday': 2, 'wednesday': 2, 'Wed': 2, 'wed': 2, 'We': 2, 'we': 2, 'W': 2, 'w': 2,
                    'Thursday':  3, 'thursday':  3, 'Thu': 3, 'thu': 3, 'Th': 3, 'th': 3, 'R': 3, 'r': 3,
                    'Friday':    4, 'friday':    4, 'Fri': 4, 'fri': 4, 'Fr': 4, 'fr': 4, 'F': 4, 'f': 4,
                    'Saturday':  5, 'saturday':  5, 'Sat': 5, 'sat': 5, 'Sa': 5, 'sa': 5, 'S': 5, 's': 5,
                    'Sunday':    6, 'sunday':    6, 'Sun': 6, 'sun': 6, 'Su': 6, 'su': 6, 'U': 6, 'u': 6, }
    return days_of_week[day]


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
        return reverse('foodcomputer:pi_list')

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

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', str(self)))
        else:
            if pre:
                bc.append(('active', pre + str(self)))
        return self.pis.all()[0].gen_breadcrumbs(bc)

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.pk):
            return True
        return False


class Pi(models.Model):
    name = models.CharField(max_length=100,)
    pi_SN = models.CharField(max_length=50, verbose_name="Serial Number",)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    manual_control = models.BooleanField(default=False,)

    tz = pytz.timezone('America/Chicago')

    def __str__(self):
        return self.name + ': ' + self.pi_SN

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

    def get_active_instance_url(self):
        ai = self.get_active_instance()
        if ai:
            return ai[0].get_absolute_url()
        return None

    def get_active_instance(self):
        instance = ExperimentInstance.objects.filter(active=True, experiment__pi__pk=self.pk)
        if instance:
            return instance
        else:
            return None

    def get_current_instance(self):
        instance = ExperimentInstance.objects.filter(start__lte=datetime.now(tz=self.tz).replace(tzinfo=None), end__gt=datetime.now(tz=self.tz).replace(tzinfo=None), experiment__pi__pk=self.pk)
        if instance:
            return instance
        else:
            return None

    def get_start_instance(self):
        instance = ExperimentInstance.objects.filter(active=False, start__lte=datetime.now(tz=self.tz).replace(tzinfo=None), end__gt=datetime.now(tz=self.tz).replace(tzinfo=None), experiment__pi__pk=self.pk)
        if instance:
            return instance
        else:
            return None

    def get_end_instance(self):
        instance = ExperimentInstance.objects.filter(Q(active=True, experiment__pi__pk=self.pk) & (Q(start__gt=datetime.now(tz=self.tz).replace(tzinfo=None)) | Q(end__lte=datetime.now(tz=self.tz).replace(tzinfo=None))))
        if instance:
            return instance
        else:
            return None

    def get_all_instances(self):
        instances = ExperimentInstance.objects.filter(experiment__pi__pk=self.pk)
        if instances:
            return instances
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

    def get_add_address_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Add Address to ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', self.name))
        else:
            if pre:
                bc.append(('active', pre + self.name))
            bc.append((self.get_absolute_url, self.name))
        bc.append((self.get_list_url, 'Food Computer List'))
        bc.append(('/', 'Home'))
        return bc

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.pk):
            return True
        return False


class Device(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE, related_name="devices",)
    device_type = models.ForeignKey('DeviceType', on_delete=models.CASCADE, related_name="devices",)
    device_id = models.CharField(max_length=50, verbose_name="Device ID",)
    residual_threshold = models.FloatField()
    deactivated = models.BooleanField(default=False)

    def __str__(self):
        return self.pi.name + ': ' + self.device_type.name + ': ' + self.device_id

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

    def get_active_baseline(self): # Assumes that 0 is Monday; oh and military time
        act_inst = self.pi.get_active_instance()
        if act_inst:
            # get rules
            rules = act_inst[0].experiment.experiment_rules.filter(device__pk=self.pk)
            if rules:
                # get the beginning of the weeks (last monday at 0:00)
                now = datetime.now(tz=None)
                start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second)

                # create dictionary of [datetime] = rule
                time2rule = {}
                for rule in rules:
                    for day in rule.days.all():
                        time2rule[start_of_week + timedelta(days=parse_day_of_week(day.name), hours=rule.hour, minutes=rule.minute)] = rule

                # determine active rule
                sd = sorted(time2rule.keys())
                prev_spot = sd.pop(0)
                for spot in sd:
                    if spot > now:
                        break
                    prev_spot = spot

                # return baseline
                return time2rule[prev_spot]
        return None

    def get_list_url(self):
        return self.pi.get_absolute_url()

    def get_threshold(self):
        return (self.residual_threshold + self.device_type.bio_threshold)

    def get_current_value(self):
        return self.data.latest('timestamp')

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', self.device_type.name))
        else:
            if pre:
                bc.append(('active', pre + self.device_type.name))
            bc.append((self.get_absolute_url, self.device_type.name))
        return self.pi.gen_breadcrumbs(bc)

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.pi.pk):
            return True
        return False


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="data",)
    timestamp = models.DateTimeField()
    data_value = models.FloatField()
    is_anomaly = models.BooleanField()

    def __str__(self):
        return str(self.timestamp) + ']: ' + str(self.data_value)

    # def get_absolute_url(self):
    #     return reverse('foodcomputer:data_detail', kwargs={'pk': self.pk})
    #
    # def get_create_url(self):
    #     return reverse('foodcomputer:data_create')
    #
    # def get_update_url(self):
    #     return reverse('foodcomputer:data_update', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('foodcomputer:data_delete', kwargs={'pk': self.pk})

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
        return self.name + ": " + self.unit_type.name

    def get_short_name(self):
        if len(self.name) > 20:
            return self.name[:20]+"..."
        else:
            return self.name

    # def get_absolute_url(self):
    #     return reverse('foodcomputer:devicetype_detail', kwargs={'pk': self.pk})
    #
    # def get_create_url(self):
    #     return reverse('foodcomputer:devicetype_create')
    #
    # def get_update_url(self):
    #     return reverse('foodcomputer:devicetype_update', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('foodcomputer:devicetype_delete', kwargs={'pk': self.pk})


class UnitType(models.Model):
    name = models.CharField(max_length=30,)
    abbr = models.CharField(max_length=10,)
    descr = models.TextField()
    min_limit = models.FloatField(blank=True, null=True,)
    max_limit = models.FloatField(blank=True, null=True,)

    def __str__(self):
        return str(self.pk) + ": " + self.name

    # def get_absolute_url(self):
    #     return reverse('foodcomputer:unittype_detail', kwargs={'pk': self.pk})
    #
    # def get_create_url(self):
    #     return reverse('foodcomputer:unittype_create')
    #
    # def get_update_url(self):
    #     return reverse('foodcomputer:unittype_update', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('foodcomputer:unittype_delete', kwargs={'pk': self.pk})


class DataType(models.Model):
    name = models.CharField(max_length=30,)
    descr = models.TextField()
    min_limit = models.FloatField(blank=True, null=True,)
    max_limit = models.FloatField(blank=True, null=True,)

    def __str__(self):
        return str(self.pk) + ": " + self.name

    # def get_absolute_url(self):
    #     return reverse('foodcomputer:pi_detail', kwargs={'pk': self.pk})
    #
    # def get_create_url(self):
    #     return reverse('foodcomputer:pi_create')
    #
    # def get_update_url(self):
    #     return reverse('foodcomputer:pi_update', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('foodcomputer:pi_delete', kwargs={'pk': self.pk})


class ControllerUpdate(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="Updates",)
    turn_on = models.BooleanField()
    timestamp = models.DateTimeField(default=datetime.now(tz=tz).replace(tzinfo=None))
    executed =models.BooleanField(default=False)
