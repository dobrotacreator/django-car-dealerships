def setup_data():
    car_model = CarModel.objects.create(name='Model X')
    car_features = CarFeatures.objects.create(year=2022, mileage=10000, gearbox='Automatic', drive='AWD',
                                              steering_wheel='Left', engine_power=250)
    dealership = Dealership.objects.create(name='ABC Motors', location='US', car_features=car_features, balance=50000)
    customer = Customer.objects.create(balance=10000, description='Regular customer', is_active=True)
    supplier = Supplier.objects.create(name='Supplier X', founding_year=2000, customer_count=1000,
                                       description='Car supplier', is_active=True)

    dealership_car_model = DealershipCarModel.objects.create(dealership=dealership, car_model=car_model, count=5)
    supplier_car_model = SupplierCarModel.objects.create(supplier=supplier, car_model=car_model)
    supplier_car_price = SupplierCarPrice.objects.create(supplier=supplier, car_model=car_model, price=25000)
    dealership_supplier_history = DealershipSupplierHistory.objects.create(dealership=dealership, supplier=supplier,
                                                                           details='Transaction details')
    customer_dealership_history = CustomerDealershipHistory.objects.create(customer=customer, dealership=dealership,
                                                                           details='Purchase details')

    yield {
        'dealership': dealership,
        'customer': customer,
        'supplier': supplier,
        'car_model': car_model,
        'dealership_supplier_history': dealership_supplier_history,
        'customer_dealership_history': customer_dealership_history,
    }


@pytest.mark.django_db
def test_models(setup_data):
    dealership = setup_data['dealership']
    customer = setup_data['customer']
    supplier = setup_data['supplier']
    car_model = setup_data['car_model']
    dealership_supplier_history = setup_data['dealership_supplier_history']
    customer_dealership_history = setup_data['customer_dealership_history']

    # Test object relationships
    assert dealership.car_models.count() == 1
    assert dealership.car_models.first().name == 'Model X'
    assert customer.purchase_history.dealership.name == 'ABC Motors'
    assert supplier.car_models.count() == 1
    assert supplier.car_models.first().name == 'Model X'

    # Test fields
    assert dealership.name == 'ABC Motors'
    assert dealership.location == 'US'
    assert dealership.balance == 50000
    assert dealership.sales_history.details == 'Transaction details'
    assert customer.balance == 10000
    assert customer.description == 'Regular customer'
    assert customer.is_active is True
    assert supplier.name == 'Supplier X'
    assert supplier.founding_year == 2000
    assert supplier.customer_count == 1000
    assert supplier.description == 'Car supplier'
    assert supplier.is_active is True
