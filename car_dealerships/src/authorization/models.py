from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        CUSTOMER = 'Customer'
        DEALERSHIP = 'Dealership'
        SUPPLIER = 'Supplier'

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.CUSTOMER)
