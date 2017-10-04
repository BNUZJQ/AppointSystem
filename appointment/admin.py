from django.contrib import admin

# Register your models here.
from appointment.models import Appointment

admin.site.register(Appointment)
