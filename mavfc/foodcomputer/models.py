from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Address(models.Model):
    street_line_1 = models.CharField(max_length=75,)
    street_line_2 = models.CharField(max_length=75,)
    city = models.CharField(max_length=30,)
    state = models.CharField(max_length=2,)
    zip = models.CharField(max_length=10,)
    
    def __str__(self):
        return "{l1}\n{l2}\n{c}, {s} {z}".format(l1=self.street_line_1, l2=self.street_line_2, c=self.city, s=self.state, z=self.zip)
    
    def get_absolute_url(self):
        return reverse('experiment:address_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:address_create')
    
    def get_update_url(self):
        return reverse('experiment:address_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:address_delete', kwargs={'pk': self.pk})


class Pi(models.Model):
    pi_SN = models.CharField(max_length=50, verbose_name="Serial Number",)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    
    def __str__(self):
        return self.pi_SN
    
    def get_absolute_url(self):
        return reverse('experiment:pi_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:pi_create')
    
    def get_update_url(self):
        return reverse('experiment:pi_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:pi_delete', kwargs={'pk': self.pk})


class Device(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE, related_name="devices",)
    device_type = models.ForeignKey('device_type', on_delete=models.CASCADE, related_name="devices",)
    device_id = models.CharField(max_length=50, verbose_name="Device ID",)
    upper_variance = models.FloatField()
    lower_variance = models.FloatField()
    
    def __str__(self):
        return self.device_id
    
    def get_absolute_url(self):
        return reverse('experiment:device_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:device_create')
    
    def get_update_url(self):
        return reverse('experiment:device_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:device_delete', kwargs={'pk': self.pk})


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="data",)
    timestamp = models.DateTimeField()
    data_value = models.FloatField()
    is_anomaly = models.BooleanField()
    
    def __str__(self):
        return '[' + self.timestamp + ']: ' + self.data_value
    
    def get_absolute_url(self):
        return reverse('experiment:data_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:data_create')
    
    def get_update_url(self):
        return reverse('experiment:data_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:data_delete', kwargs={'pk': self.pk})


class Device_Type(models.Model):
    unit_type = models.ForeignKey('Unit_Type', on_delete=models.CASCADE, related_name="device_types",)
    data_type = models.ForeignKey('Data_Type', on_delete=models.CASCADE, related_name="device_types",)
    is_controller = models.BooleanField()
    
    def __str__(self):
        return self.pi_SN
    
    def get_absolute_url(self):
        return reverse('experiment:devicetype_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:devicetype_create')
    
    def get_update_url(self):
        return reverse('experiment:devicetype_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:devicetype_delete', kwargs={'pk': self.pk})


class Unit_Type(models.Model):
    name = models.CharField(max_length=30,)
    abbr = models.CharField(max_length=10,)
    descr = models.TextField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('experiment:unittype_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:unittype_create')
    
    def get_update_url(self):
        return reverse('experiment:unittype_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:unittype_delete', kwargs={'pk': self.pk})


class Data_Type(models.Model):
    name = models.CharField(max_length=30,)
    descr = models.TextField()
    min_limit = models.FloatField()
    max_limit = models.FloatField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('experiment:pi_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('experiment:pi_create')
    
    def get_update_url(self):
        return reverse('experiment:pi_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('experiment:pi_delete', kwargs={'pk': self.pk})




















