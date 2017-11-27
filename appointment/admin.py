from django.contrib import admin

# Register your models here.
from appointment.models import Appointment, STATUS

class AppointmentAdmin(admin.ModelAdmin):
    #list_display_fields = ('user','student_id','grade','major',)
    list_display = ('id','custom','date','start','end','reason',)
    list_filter = ('classroom','date','boss','custom__user__username',)
    search_fields = ('custom__user__username','classroom','boss',)

# Register your models here.
admin.site.register(Appointment, AppointmentAdmin)

