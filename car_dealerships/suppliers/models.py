from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    founding_year = models.PositiveIntegerField()
    customer_count = models.PositiveIntegerField()
    description = models.TextField()
    car_models = models.ManyToManyField('cars.CarModel', through='SupplierCarModel',
                                        related_name='suppliers_car_models')
    car_prices = models.ManyToManyField('cars.CarModel', through='SupplierCarPrice',
                                        related_name='suppliers_car_prices')
    sales_history = models.ForeignKey('transaction_history.DealershipSupplierHistory', on_delete=models.CASCADE,
                                      related_name='supplier_sales_history')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SupplierCarModel(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE)


class SupplierCarPrice(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
