# coding=utf-8
from rest_framework import viewsets, permissions, authentication, filters
from Account.models import Account


class AccountViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
