from django.contrib import admin
from django.db.models import Sum

from src.customers.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_spent', 'get_purchased_cars_count')

    @staticmethod
    def get_total_spent(obj):
        return obj.purchase_history.aggregate(total_spent=Sum('dealership__dealershipcarmodel__price'))['total_spent']

    @staticmethod
    def get_purchased_cars_count(obj):
        return obj.purchase_history.count()


admin.site.register(Customer, CustomerAdmin)
