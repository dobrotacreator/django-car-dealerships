from django.db import models


class CarModel(models.Model):
    name = models.CharField(max_length=255)


class CarFeatures(models.Model):
    year = models.IntegerField()
    mileage = models.DecimalField(max_digits=10, decimal_places=2)
    gearbox = models.CharField(max_length=100)
    drive = models.CharField(max_length=100)
    steering_wheel = models.CharField(max_length=100)
    engine_power = models.DecimalField(max_digits=10, decimal_places=2)
