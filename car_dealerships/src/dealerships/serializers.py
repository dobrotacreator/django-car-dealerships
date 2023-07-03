from rest_framework import serializers

from src.authorization.serializers import UserSerializer
from src.cars.serializers import CarFeaturesSerializer, CarModelSerializer
from .models import Dealership


class DealershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    car_features = CarFeaturesSerializer()
    car_models = CarModelSerializer()

    class Meta:
        model = Dealership
        fields = '__all__'
        read_only_fields = ['id', 'user', 'balance', 'sales_history', 'customers']
