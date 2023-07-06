import pytest

from src.authorization.models import User
from src.cars.models import CarFeatures, CarModel
from src.dealerships.models import Dealership
from src.dealerships.tasks import purchase_cars
from src.suppliers.models import SupplierCarModel, Supplier
from src.transaction_history.models import DealershipSupplierHistory


@pytest.fixture
def car_features():
    return CarFeatures.objects.create(color='R', year=2020, mileage=5000, vin_number="1GNEK13ZX3R298984")


@pytest.fixture
def car_model(car_features):
    return CarModel.objects.create(name='Model 1', features=car_features)


@pytest.fixture
def dealership(car_features):
    user = User.objects.create(username="dealership", email="example1@example.com", password="dealership",
                               role="Dealership", is_active=True)
    return Dealership.objects.create(user=user, name="test_dealer", location="NZ", car_features=car_features,
                                     balance=14000)


@pytest.fixture
def supplier(car_model):
    user = User.objects.create(username="supplier", email="example2@example.com", password="supplier", role="Supplier",
                               is_active=True)
    supplier = Supplier.objects.create(user=user, name="test_supplier", founding_year=2000, description="Aaa")
    supplier_car_model = SupplierCarModel.objects.create(supplier=supplier, car_model=car_model, price=5000)
    supplier.suppliercarmodel_set.add(supplier_car_model)
    return supplier


@pytest.mark.django_db
def test_purchase_cars(dealership, supplier):
    # Run the purchase_cars task
    purchase_cars()

    # Refresh the dealership and supplier car model from the database
    dealership.refresh_from_db()
    supplier.refresh_from_db()

    # Assert that the dealership's balance is updated correctly
    assert dealership.balance == 9000

    # Assert that the dealership's sales history is updated correctly
    assert dealership.purchase_history.count() == 1

    dealership.user.delete()
    dealership.delete()
    supplier.user.delete()
    supplier.delete()
