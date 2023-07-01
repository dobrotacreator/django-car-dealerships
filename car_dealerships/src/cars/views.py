from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdmin, ReadOnly
from .models import CarModel
from .serializers import CarModelSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = (IsAuthenticated, IsAdmin | ReadOnly)
