from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import MaintenanceLog

admin.site.register(MaintenanceLog)
admin.site.site_url = "/dashboard/"