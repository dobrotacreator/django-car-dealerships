import django_filters

from .models import Dealership
from src.cars.models import CarFeatures


class DealershipFilter(django_filters.FilterSet):
    car_models__name = django_filters.CharFilter(
        field_name='car_models__name',
        lookup_expr='icontains'
    )
    car_models__car_features__color = django_filters.ChoiceFilter(
        field_name='car_models__car_features__color',
        choices=CarFeatures.Color.choices
    )
    car_models__car_features__year = django_filters.NumberFilter(
        field_name='car_models__car_features__year'
    )
    car_models__car_features__mileage = django_filters.NumberFilter(
        field_name='car_models__car_features__mileage'
    )
    car_models__car_features__gearbox = django_filters.CharFilter(
        field_name='car_models__car_features__gearbox',
        lookup_expr='icontains'
    )
    car_models__car_features__drive = django_filters.CharFilter(
        field_name='car_models__car_features__drive',
        lookup_expr='icontains'
    )
    car_models__car_features__steering_wheel = django_filters.CharFilter(
        field_name='car_models__car_features__steering_wheel',
        lookup_expr='icontains'
    )
    car_models__car_features__engine_power = django_filters.NumberFilter(
        field_name='car_models__car_features__engine_power'
    )
    car_models__car_features__vin_number = django_filters.CharFilter(
        field_name='car_models__car_features__vin_number',
        lookup_expr='exact'
    )

    class Meta:
        model = Dealership
        fields = [
            'car_models', 'car_models__name', 'car_models__car_features__color', 'car_models__car_features__year',
            'car_models__car_features__mileage', 'car_models__car_features__gearbox',
            'car_models__car_features__drive', 'car_models__car_features__steering_wheel',
            'car_models__car_features__engine_power', 'car_models__car_features__vin_number'
        ]
