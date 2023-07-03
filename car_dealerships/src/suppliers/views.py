from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin, ReadOnly, IsOwner, CreateAndReadOnly
from .permissions import IsSupplier
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner | IsSupplier & CreateAndReadOnly | ReadOnly)

    def create(self, request, *args, **kwargs):
        # + Define the owner of instance
        request.data['user'] = request.user.pk

        # Create a new serializer instance with the modified validated data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['user'] = request.user

        # Save the serializer instance to create the Dealership object
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
