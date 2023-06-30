from django.db import models
from django_countries import fields


class Dealership(models.Model):
    name = models.CharField(max_length=255)
    location = fields.CountryField()
    car_features = models.OneToOneField('cars.CarFeatures', on_delete=models.CASCADE)
    car_models = models.ManyToManyField('cars.CarModel', through='DealershipCarModel')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    sales_history = models.ForeignKey('transaction_history.DealershipSupplierHistory', on_delete=models.CASCADE,
                                      related_name='dealership_sales_history')
    customers = models.ManyToManyField('customers.Customer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DealershipCarModel(models.Model):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
