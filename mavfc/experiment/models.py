from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Experiment(models.Model):
    name = models.CharField(max_length=200,)
    descr = models.TextField()
    pi = models.ForeignKey('foodcomputer.Pi', on_delete=models.CASCADE, related_name="experiment",)
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

    def get_breadcrumbs(self):
        return self.gen_breadcrumbs(bc=[])

    def gen_breadcrumbs(self, bc=[]):
        if bc == []:
            bc.append(('active', self.name))
        else:
            bc.append((self.get_absolute_url, self.name))
        bc.append((self.get_list_url, 'Experiment List'))
        bc.append(('/home/', 'Home'))
        return bc


class Day(models.Model):
    name = models.CharField(max_length=9,)
    
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
    device = models.ForeignKey('foodcomputer.Device', on_delete=models.CASCADE, related_name="device_rules",)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="experiment_rules",)
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

    def gen_breadcrumbs(self, bc=[]):
        if bc == []:
            bc.append(('active', self.device.device_type.name + ' Rule'))
        else:
            bc.append((self.get_absolute_url, self.device.device_type.name + ' Rule'))
        return self.experiment.gen_breadcrumbs(bc)


class ExperimentInstance(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="instances",)
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

    def gen_breadcrumbs(self, bc=[]):
        if bc == []:
            bc.append(('active', self.start.strftime("%m/%d/%y") + ' - ' + self.end.strftime("%m/%d/%y") + ' Instance'))

        else:
            bc.append((self.get_absolute_url, self.start.strftime("%m/%d/%y") + ' - ' + self.end.strftime("%m/%d/%y") + 'Instance'))
        return self.experiment.gen_breadcrumbs(bc)


class UserExperimentInstance(models.Model):
    experiment_instance = models.ForeignKey(ExperimentInstance, on_delete=models.CASCADE, related_name="instance_users",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="experiment_instances",)
    is_user = models.BooleanField()
    
    def __str__(self):
        return self.experiment_instance.pi.name + ": " + self.user.get_username
    
   #def get_absolute_url(self):
        #return reverse('experiment:userexperimentinstance_detail', kwargs={'pk': self.pk})
    
   # def get_create_url(self):
        #return reverse('experiment:userexperimentinstance_create')
    
    #def get_update_url(self):
       # return reverse('experiment:userexperimentinstance_update', kwargs={'pk': self.pk})
    
    #def get_delete_url(self):
        #return reverse('experiment:userexperimentinstance_delete', kwargs={'pk': self.pk})

    
    
    
    
    
    
    
    