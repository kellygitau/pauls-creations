from django.contrib import admin

from .models import *
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# admin.site.register(PeriodicTask)
# admin.site.register(CrontabSchedule)

admin.site.register(Vendors)
admin.site.register(VendorOrder)
admin.site.register(Material)
