from django.db import models

from core.base_models import BaseModel


class Supplier(BaseModel):
    user = models.OneToOneField('authorization.User', on_delete=models.CASCADE, related_name='supplier')
    name = models.CharField(max_length=255)
    founding_year = models.PositiveIntegerField()
    description = models.TextField()
    car_models = models.ManyToManyField('cars.CarModel', through='SupplierCarModel',
                                        related_name='suppliers_car_models')


class SupplierCarModel(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=100000000)
    updated_at = models.DateTimeField(auto_now=True)
