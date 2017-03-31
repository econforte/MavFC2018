from django.contrib import admin
from .models import *

admin.site.register(Address)
admin.site.register(Pi)
admin.site.register(Device)
admin.site.register(Data)
admin.site.register(DeviceType)
admin.site.register(UnitType)
admin.site.register(DataType)
admin.site.register(ControllerUpdate)