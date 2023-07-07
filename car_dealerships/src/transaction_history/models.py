from django.db import models


class DealershipSupplierHistory(models.Model):
    dealership = models.ForeignKey('dealerships.Dealership', on_delete=models.CASCADE, related_name='purchase_history')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='sales_history')
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CustomerDealershipHistory(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='purchase_history')
    dealership = models.ForeignKey('dealerships.Dealership', on_delete=models.CASCADE, related_name='sales_history')
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
