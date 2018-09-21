#coding=utf-8
from django.contrib import admin

# Register your models here.
from appointment.models import Appointment, STATUS

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id','custom','date','start','end','reason','status',)
    list_filter = ('classroom','date','status','boss','custom__user__username',)
    search_fields = ('custom__user__username','classroom','boss',)
    actions = ['cancel','activate',]

    def cancel(self, request, queryset):
        queryset.update(status=STATUS.canceled)
        self.message_user(request, '选中预约已被取消')
    cancel.short_description = '取消选定预约'

    def activate(self, request, queryset):
        queryset.update(status=STATUS.waiting)
        self.message_user(request, '选中预约已被激活')
    activate.short_description = '激活选中预约'

# Register your models here.
admin.site.register(Appointment, AppointmentAdmin)

