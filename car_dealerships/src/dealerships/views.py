from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdmin, ReadOnly, IsOwner
from .models import Dealership
from .serializers import DealershipSerializer


class DealershipViewSet(viewsets.ModelViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner | ReadOnly)
