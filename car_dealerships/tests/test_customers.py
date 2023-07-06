import pytest

from src.authorization.models import User
from src.cars.models import CarFeatures, CarModel
from src.customers.models import Customer
from src.dealerships.models import Dealership, DealershipCarModel
from src.customers.tasks import process_offer_creation


@pytest.fixture
def car_features():
    return CarFeatures.objects.create(color='R', year=2020, mileage=5000, vin_number="1GNEK13ZX3R298984")


@pytest.fixture
def car_model(car_features):
    return CarModel.objects.create(name='Model 1', features=car_features)


@pytest.fixture
def dealership(car_features, car_model):
    user = User.objects.create(username="dealership", email="example@example.com", password="dealership",
                               role="Dealership", is_active=True)
    dealership = Dealership.objects.create(user=user, name="test_dealer", location="NZ", car_features=car_features,
                                           balance=14000)
    dealership_car_model = DealershipCarModel.objects.create(
        dealership=dealership,
        car_model=car_model,
        price=6000,
        count=1
    )
    dealership.dealershipcarmodel_set.add(dealership_car_model)

    return dealership


@pytest.fixture
def customer():
    user = User.objects.create(username="customer", email="example1@example.com", password="customer",
                               role="Customer", is_active=True)
    return Customer.objects.create(user=user, balance=140000, description="customer")


@pytest.mark.django_db
def test_process_offer_creation(dealership, customer, car_features):
    # Call the Celery task
    task_result = process_offer_creation(
        max_price=6000,
        car_features=car_features,
        customer_id=customer.id
    )

    # Check the task result
    assert task_result['message'] == 'Offer created successfully.'

    dealership.user.delete()
    dealership.car_models.all().delete()
    car_features.delete()
    dealership.delete()
    customer.user.delete()
    customer.delete()
