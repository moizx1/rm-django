from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'account_number', 'balance', 'created_at']
        read_only = ['balance', 'created_at']
