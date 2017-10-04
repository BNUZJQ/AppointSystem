# coding=utf-8
from rest_framework import viewsets, permissions, authentication, filters
from Account.models import Account
from Account.serializer import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
