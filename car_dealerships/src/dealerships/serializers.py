from rest_framework import serializers

from .models import Dealership


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = '__all__'
        read_only_fields = ['id', 'balance', 'sales_history', 'customers']
