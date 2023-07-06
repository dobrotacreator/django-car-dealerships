from celery import shared_task

from src.dealerships.services import CarPurchaseService


@shared_task
def purchase_cars():
    CarPurchaseService.purchase_cars()
