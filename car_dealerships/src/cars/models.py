from django.core.validators import RegexValidator
from django.db import models


class CarModel(models.Model):
    name = models.CharField(max_length=255)


class CarFeatures(models.Model):
    class Color(models.TextChoices):
        RED = 'R', 'Red'
        BLUE = 'B', 'Blue'
        GREEN = 'G', 'Green'
        YELLOW = 'Y', 'Yellow'
        BLACK = 'BL', 'Black'
        WHITE = 'WH', 'White'
        SILVER = 'S', 'Silver'
        ORANGE = 'O', 'Orange'
        PURPLE = 'P', 'Purple'

    color = models.CharField(max_length=10, choices=Color.choices)
    year = models.PositiveIntegerField()
    mileage = models.DecimalField(max_digits=10, decimal_places=2)
    gearbox = models.CharField(max_length=100)
    drive = models.CharField(max_length=100)
    steering_wheel = models.CharField(max_length=100)
    engine_power = models.DecimalField(max_digits=10, decimal_places=2)
    vin_number = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^[A-HJ-NPR-Z0-9]{17}$',
                message='VIN number must be a valid 17-character VIN',
                code='invalid_vin'
            )
        ]
    )
