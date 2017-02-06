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
        return reverse('foodcomputer:address_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('foodcomputer:address_create')
    
    def get_update_url(self):
        return reverse('foodcomputer:address_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('foodcomputer:address_delete', kwargs={'pk': self.pk})


class Pi(models.Model):
    pi_SN = models.CharField(max_length=50, verbose_name="Serial Number",)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="pis",)
    
    def __str__(self):
        return self.pi_SN
    
    def get_absolute_url(self):
        return reverse('foodcomputer:pi_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('foodcomputer:pi_create')
    
    def get_update_url(self):
        return reverse('foodcomputer:pi_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('foodcomputer:pi_delete', kwargs={'pk': self.pk})


class Device(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE, related_name="devices",)
    device_type = models.ForeignKey('DeviceType', on_delete=models.CASCADE, related_name="devices",)
    device_id = models.CharField(max_length=50, verbose_name="Device ID",)
    upper_variance = models.FloatField()
    lower_variance = models.FloatField()
    
    def __str__(self):
        return self.device_id
    
    def get_absolute_url(self):
        return reverse('foodcomputer:device_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('foodcomputer:device_create')
    
    def get_update_url(self):
        return reverse('foodcomputer:device_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('foodcomputer:device_delete', kwargs={'pk': self.pk})


class Data(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="data",)
    timestamp = models.DateTimeField()
    data_value = models.FloatField()
    is_anomaly = models.BooleanField()
    
    def __str__(self):
        return '[' + self.timestamp + ']: ' + self.data_value
    
    def get_absolute_url(self):
        return reverse('foodcomputer:data_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('foodcomputer:data_create')
    
    def get_update_url(self):
        return reverse('foodcomputer:data_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('foodcomputer:data_delete', kwargs={'pk': self.pk})


class DeviceType(models.Model):
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, related_name="device_types",)
    data_type = models.ForeignKey('DataType', on_delete=models.CASCADE, related_name="device_types",)
    is_controller = models.BooleanField()
    
    def __str__(self):
        return self.pi_SN
    
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
    
    def __str__(self):
        return self.name
    
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
    min_limit = models.FloatField()
    max_limit = models.FloatField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('foodcomputer:pi_detail', kwargs={'pk': self.pk})
    
    def get_create_url(self):
        return reverse('foodcomputer:pi_create')
    
    def get_update_url(self):
        return reverse('foodcomputer:pi_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('foodcomputer:pi_delete', kwargs={'pk': self.pk})




















