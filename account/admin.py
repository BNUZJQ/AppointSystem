#coding=utf-8
from django.contrib import admin
from account.models import Account
from django.contrib.auth.models import User

class AccountAdmin(admin.ModelAdmin):
    #list_display_fields = ('user','student_id','grade','major',)
    list_display = ('user','student_id','telephone','grade','major',)
    list_filter = ('grade','completed','user__is_active','major',)
    search_fields = ('user__username','student_id',)
    actions = ['blacklist','activate','completed']

    def blacklist(self, request, queryset):
        for query in queryset:
            user = query.user
            user.is_active = False
            user.save()
        self.message_user(request, '选中用户已被加入黑名单')
    blacklist.short_description = '加入黑名单'

    def activate(self, request, queryset):
        for query in queryset:
            user = query.user
            user.is_active = True
            user.save()
        self.message_user(request, '选中用户已被移出黑名单')
    activate.short_description = '移出黑名单'

    def completed(self, request, queryset):
        queryset.update(completed = False)
        self.message_user(request, '选中用户已被要求修改信息')
    completed.short_description = '要求用户修改信息'

# Register your models here.
admin.site.register(Account, AccountAdmin)