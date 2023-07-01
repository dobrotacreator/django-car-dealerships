import pytest

from src.authorization.models import User
from src.cars.models import CarModel, CarFeatures
from src.customers.models import Customer
from src.dealerships.models import Dealership, DealershipCarModel
from src.suppliers.models import Supplier, SupplierCarModel
from src.transaction_history.models import DealershipSupplierHistory, CustomerDealershipHistory


@pytest.fixture
def setup_data():
    # Create CarModel objects
    car_model1 = CarModel.objects.create(name='Model 1')
    car_model2 = CarModel.objects.create(name='Model 2')

    # Create a Customer instance
    user_customer = User.objects.create_user(username='customer1', password='password', role=User.Roles.CUSTOMER)

    # Create a Dealership instance
    user_dealership = User.objects.create_user(username='dealership1', password='password', role=User.Roles.DEALERSHIP)

    # Create a Supplier instance
    user_supplier = User.objects.create_user(username='supplier1', password='password', role=User.Roles.SUPPLIER)

    # Create CarFeatures objects
    car_features1 = CarFeatures.objects.create(
        color=CarFeatures.Color.RED,
        year=2022,
        mileage=10000,
        gearbox='Automatic',
        drive='FWD',
        steering_wheel='Left',
        engine_power=200,
        vin_number='ABCDE12345FGHIJKL'
    )
    car_features2 = CarFeatures.objects.create(
        color=CarFeatures.Color.BLUE,
        year=2021,
        mileage=20000,
        gearbox='Manual',
        drive='RWD',
        steering_wheel='Right',
        engine_power=180,
        vin_number='FGHIJKL12345ABCDE'
    )

    # Create Dealership objects
    dealership = Dealership.objects.create(
        user=user_dealership,
        name='Test Dealership',
        location='US',
        car_features=car_features1,
        balance=100000,
        is_active=True
    )
    dealership.car_models.add(car_model1, through_defaults={'count': 5})
    dealership.car_models.add(car_model2, through_defaults={'count': 10})

    # Create Customer object
    customer = Customer.objects.create(
        user=user_customer,
        balance=50000,
        description='Test customer',
        is_active=True
    )
    customer.purchase_history = CustomerDealershipHistory.objects.create(
        customer=customer,
        dealership=dealership,
        details='Purchase history details'
    )

    # Create Supplier object
    supplier = Supplier.objects.create(
        user=user_supplier,
        name='Test Supplier',
        founding_year=2000,
        description='Test supplier',
        is_active=True
    )
    supplier.sales_history = DealershipSupplierHistory.objects.create(
        dealership=dealership,
        supplier=supplier,
        details='Sales history details'
    )
    supplier.car_models.add(car_model1, through_defaults={'price': 20000, 'count': 50})

    dealership.sales_history = DealershipSupplierHistory.objects.create(
        dealership=dealership,
        supplier=supplier,
        details='Sales history details'
    )

    yield {
        'dealership': dealership,
        'car_model1': car_model1,
        'car_model2': car_model2,
        'car_features1': car_features1,
        'car_features2': car_features2,
        'customer': customer,
        'supplier': supplier,
    }

    # Clean up the created objects after the tests
    user_supplier.delete()
    user_customer.delete()
    user_dealership.delete()
    dealership.delete()
    car_model1.delete()
    car_model2.delete()
    car_features1.delete()
    car_features2.delete()
    supplier.delete()
    customer.delete()


@pytest.mark.django_db
def test_dealership_car_models(setup_data):
    dealership = setup_data['dealership']
    car_model1 = setup_data['car_model1']
    car_model2 = setup_data['car_model2']

    assert dealership.car_models.count() == 2
    assert car_model1 in dealership.car_models.all()
    assert car_model2 in dealership.car_models.all()
    assert DealershipCarModel.objects.get(dealership=dealership, car_model=car_model1).count == 5
    assert DealershipCarModel.objects.get(dealership=dealership, car_model=car_model2).count == 10


@pytest.mark.django_db
def test_supplier_car_models(setup_data):
    supplier = setup_data['supplier']
    car_model1 = setup_data['car_model1']

    assert supplier.car_models.count() == 1
    assert car_model1 in supplier.car_models.all()
    assert SupplierCarModel.objects.get(supplier=supplier, car_model=car_model1).count == 50
    assert SupplierCarModel.objects.get(supplier=supplier, car_model=car_model1).price == 20000
