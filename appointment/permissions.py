from rest_framework import permissions

from account.models import Account, ROLE


class AppointmentPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        if request.user is None or request.user.is_authenticated() is False:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        account = Account.objects.get(user=request.user)
        if account.role != ROLE.Blacklist:
            return True
        return False
