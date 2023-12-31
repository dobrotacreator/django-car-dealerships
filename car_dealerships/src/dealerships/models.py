from django.db import models
from django_countries import fields

from core.base_models import BaseModel


class Dealership(BaseModel):
    user = models.OneToOneField('authorization.User', on_delete=models.CASCADE, related_name='dealership')
    name = models.CharField(max_length=255)
    location = fields.CountryField()
    car_features = models.OneToOneField('cars.CarFeatures', on_delete=models.CASCADE)
    car_models = models.ManyToManyField('cars.CarModel', through='DealershipCarModel')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customers = models.ManyToManyField('customers.Customer')


class DealershipCarModel(models.Model):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField()
