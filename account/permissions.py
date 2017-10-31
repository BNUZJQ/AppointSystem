from rest_framework import permissions


class AccountPermission(permissions.BasePermission):
    message = 'Permission Denied'

    def has_permission(self, request, view):
        if request.user is None or request.user.is_authenticated() is False:
            return False
        # account = Account.objects.get(user=request.user)
        # if account.role != ROLE.Teacher:
        #     return False
        return True
