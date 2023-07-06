from celery import shared_task

from src.customers.services import OfferService


@shared_task
def process_offer_creation(max_price: int, car_features, customer_id: int):
    return OfferService.process_offer_creation(max_price=max_price, car_features=car_features, customer_id=customer_id)
