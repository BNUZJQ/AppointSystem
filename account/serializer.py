from rest_framework import serializers
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = '__all__'
