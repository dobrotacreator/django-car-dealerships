from django.db import models


class Customer(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_history = models.ForeignKey('transaction_history.CustomerDealershipHistory', on_delete=models.CASCADE,
                                         related_name='customer_purchase_history')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
