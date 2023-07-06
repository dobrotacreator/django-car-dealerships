from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin, ReadOnly, IsOwner, CreateAndReadOnly
from .permissions import IsCustomer
from .models import Customer
from .serializers import CustomerSerializer
from .tasks import process_offer_creation
from ..cars.serializers import CarFeaturesSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner | IsCustomer & CreateAndReadOnly | ReadOnly)

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

    @action(detail=False, methods=['post'])
    def offer(self, request):
        # Retrieve the necessary data from the request
        max_price = request.data.get('max_price')
        car_features_data = request.data.get('car_features')
        serializer = CarFeaturesSerializer(data=car_features_data)
        serializer.is_valid(raise_exception=True)
        car_features = serializer.data
        customer_id = request.user.customer.id

        # Invoke the Celery task asynchronously
        task_result = process_offer_creation.delay(max_price, car_features, customer_id)

        # Return an immediate response indicating the task has started
        return Response({'message': 'Offer creation started.', 'offer_id': task_result.id}, status=202)

    @offer.mapping.get
    def check_offer(self, request, offer_id):
        # Get the task result using the offer_id
        task_result = process_offer_creation.AsyncResult(offer_id)

        # Check the task status
        task_status = task_result.state

        # Handle the task result based on its status
        if task_status == 'SUCCESS':
            task_result_data = task_result.get()
            return Response(task_result_data, status=200)
        elif task_status in ['PENDING', 'STARTED']:
            return Response({'message': 'Task is still in progress.'}, status=202)
        else:
            return Response({'message': 'Task failed.'}, status=500)
