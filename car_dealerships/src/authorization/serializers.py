from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'role']
        read_only_fields = ['id', 'username', 'email', 'is_active']

    def update(self, instance, validated_data):
        # Exclude 'role' field from update
        validated_data.pop('role', None)
        return super().update(instance, validated_data)
