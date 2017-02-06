from django.contrib import admin
from .models import *


admin.site.register(Experiment)
admin.site.register(ExperimentRule)
admin.site.register(Day)
admin.site.register(ExperimentInstance)
admin.site.register(UserExperimentInstance)