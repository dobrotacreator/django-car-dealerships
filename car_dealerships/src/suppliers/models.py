from django.db import models

from core.base_models import BaseModel


class Supplier(BaseModel):
    name = models.CharField(max_length=255)
    founding_year = models.PositiveIntegerField()
    description = models.TextField()
    car_models = models.ManyToManyField('cars.CarModel', through='SupplierCarModel',
                                        related_name='suppliers_car_models')
    sales_history = models.ForeignKey('transaction_history.DealershipSupplierHistory', on_delete=models.CASCADE,
                                      related_name='supplier_sales_history', null=True, blank=True)


class SupplierCarModel(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
