from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.cars.serializers import CarFeaturesSerializer
from core.permissions import IsAdmin, CreateAndReadOnly, IsOwner, ReadOnly
from .permissions import IsDealership
from .filters import DealershipFilter
from .models import Dealership
from .serializers import DealershipSerializer


class DealershipViewSet(viewsets.ModelViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner | IsDealership & CreateAndReadOnly | ReadOnly)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = DealershipFilter
    ordering_fields = ['car_models__price', 'car_models__count', ]
    search_fields = ['car_models__name', ]

    def create(self, request, *args, **kwargs):
        # Related CarFeatures object will be created and associated with the Dealership object
        car_features_data = request.data.get('car_features')
        car_features_serializer = CarFeaturesSerializer(data=car_features_data)
        car_features_serializer.is_valid(raise_exception=True)
        car_features = car_features_serializer.save()

        # + Define the owner of instance
        request.data['user'] = request.user.pk

        # Create a new serializer instance with the modified validated data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['user'] = request.user
        serializer.validated_data['car_features'] = car_features

        # Save the serializer instance to create the Dealership object
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
