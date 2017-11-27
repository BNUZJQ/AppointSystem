from django.contrib import admin
from account.models import Account


class AccountAdmin(admin.ModelAdmin):
    #list_display_fields = ('user','student_id','grade','major',)
    list_display = ('user','student_id','grade','major',)
    list_filter = ('grade','completed')
    search_fields = ('user__username','student_id',)

# Register your models here.
admin.site.register(Account, AccountAdmin)