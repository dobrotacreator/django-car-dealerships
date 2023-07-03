from django.db import models

from core.base_models import BaseModel


class Customer(BaseModel):
    user = models.OneToOneField('authorization.User', on_delete=models.CASCADE, related_name='customer')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_history = models.ForeignKey('transaction_history.CustomerDealershipHistory', on_delete=models.CASCADE,
                                         related_name='customer_purchase_history', null=True, blank=True)
    description = models.TextField()
