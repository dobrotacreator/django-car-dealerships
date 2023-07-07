from django.contrib import admin
from django.db.models import Sum

from src.dealerships.models import Dealership


class DealershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_sold_cars_count', 'get_total_revenue', 'get_unique_customers_count')

    @staticmethod
    def get_sold_cars_count(obj):
        return obj.sales_history.count()

    @staticmethod
    def get_total_revenue(obj):
        return obj.sales_history.aggregate(total_revenue=Sum('dealershipcarmodel__price'))['total_revenue']

    @staticmethod
    def get_unique_customers_count(obj):
        return obj.customers.count()


admin.site.register(Dealership, DealershipAdmin)
