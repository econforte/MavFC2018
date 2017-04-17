from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q


class Experiment(models.Model):
    name = models.CharField(max_length=200, )
    descr = models.TextField()
    pi = models.ForeignKey('foodcomputer.Pi', on_delete=models.CASCADE, related_name="experiment", )
    collection_interval = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('experiment:experiment_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('experiment:experiment_create')

    def get_update_url(self):
        return reverse('experiment:experiment_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('experiment:experiment_delete', kwargs={'pk': self.pk})

    def get_list_url(self):
        return reverse('experiment:experiment_list')

    def get_pi(self):
        return self.experiment_rules[:1].device.pi

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def get_add_rule_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Add Rule to ")

    def get_add_inst_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Create Instance of ")

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', self.name))
        else:
            if pre:
                bc.append(('active', pre + self.name))
            bc.append((self.get_absolute_url, self.name))
        bc.append((self.get_list_url, 'Experiment List'))
        bc.append(('/', 'Home'))
        return bc

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.pi.pk):
            return True
        return False


class Day(models.Model):
    name = models.CharField(max_length=9, )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('experiment:day_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('experiment:day_create')

    def get_update_url(self):
        return reverse('experiment:day_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('experiment:day_delete', kwargs={'pk': self.pk})


class ExperimentRule(models.Model):
    device = models.ForeignKey('foodcomputer.Device', on_delete=models.CASCADE, related_name="device_rules", )
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="experiment_rules", )
    hour = models.IntegerField()
    minute = models.IntegerField()
    baseline_target = models.FloatField()
    days = models.ManyToManyField(Day)

    def __str__(self):
        return self.experiment.name + ': ' + self.device.device_type.name + ' Rule'

    def get_absolute_url(self):
        return reverse('experiment:experimentrule_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('experiment:experimentrule_create')

    def get_update_url(self):
        return reverse('experiment:experimentrule_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('experiment:experimentrule_delete', kwargs={'pk': self.pk})

    def get_threshold(self):
        return (self.device.residual_threshold + self.device.device_type.bio_threshold)

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', self.device.device_type.name + ' Rule'))
        else:
            if pre:
                bc.append(('active', pre + self.device.device_type.name + ' Rule'))
            bc.append((self.get_absolute_url, self.device.device_type.name + ' Rule'))
        return self.experiment.gen_breadcrumbs(bc)

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.experiment.pi.pk):
            return True
        return False


class ExperimentInstance(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="instances", )
    start = models.DateTimeField()
    end = models.DateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.experiment.name + ': ' + str(self.start) + ' - ' + str(self.end)

    def get_absolute_url(self):
        return reverse('experiment:experimentinstance_detail', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('experiment:experimentinstance_create')

    def get_update_url(self):
        return reverse('experiment:experimentinstance_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('experiment:experimentinstance_delete', kwargs={'pk': self.pk})

    def get_csv_url(self):
        return reverse('experiment:experimentinstance_get_csv', kwargs={'pk': self.pk})

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def get_add_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Add User For ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', self.start.strftime("%m/%d/%y") + ' - ' + self.end.strftime("%m/%d/%y") + ' Instance'))
        else:
            if pre:
                bc.append(('active', pre + self.start.strftime("%m/%d/%y") + ' - ' + self.end.strftime("%m/%d/%y") + ' Instance'))
            bc.append((self.get_absolute_url, self.start.strftime("%m/%d/%y") + ' - ' + self.end.strftime("%m/%d/%y") + 'Instance'))
        return self.experiment.gen_breadcrumbs(bc)

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.experiment.pi.pk):
            return True
        return False


class UserExperimentInstance(models.Model):
    experiment_instance = models.ForeignKey(ExperimentInstance, on_delete=models.CASCADE, related_name="instance_users", )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="experiment_instances", )
    is_user = models.BooleanField()

    def __str__(self):
        return self.experiment_instance.experiment.name + ": " + self.user.username

    def get_absolute_url(self):
        return self.experiment_instance.get_absolute_url()

    def get_create_url(self):
        return reverse('experiment:user_experimentinstance_add', kwargs={'pk': self.experiment_instance.pk})

    def get_update_url(self):
        return reverse('experiment:user_experimentinstance_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('experiment:user_experimentinstance_delete', kwargs={'pk': self.pk})

    def get_add_url(self):
        return reverse('experiment:user_experimentinstance_add', kwargs={'pk': self.experiment_instance.pk})

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def get_update_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Update ")

    def get_delete_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[], pre="Delete ")

    def gen_breadcrumbs(self, bc=[], pre=""):
        if bc == [] and not pre:
            bc.append(('active', str(self.user)))
        else:
            if pre:
                bc.append(('active', pre + str(self.user)))
            # bc.append((self.get_absolute_url, str(self.user)))
        return self.experiment_instance.gen_breadcrumbs(bc)

    def user_cud_authorized(self, user):
        if user.is_staff or user.pis.filter(pk=self.experiment_instance.experiment.pi.pk):
            return True
        return False
