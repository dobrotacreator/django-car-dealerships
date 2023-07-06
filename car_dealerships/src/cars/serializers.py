from rest_framework import serializers

from .models import CarModel, CarFeatures


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'


class CarFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFeatures
        fields = '__all__'
