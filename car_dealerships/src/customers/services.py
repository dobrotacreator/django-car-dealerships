from django.db.models import F, Q

from src.customers.models import Customer
from src.dealerships.models import DealershipCarModel
from src.transaction_history.models import CustomerDealershipHistory


class OfferService:
    @staticmethod
    def process_offer_creation(max_price: int, car_features, customer_id: int) -> dict:
        """
        Process the creation of an offer based on the provided parameters.

        Args:
            max_price (int): The maximum price of the offer.
            car_features (CarFeatures): The car features object representing the desired features.
            customer_id (int): The ID of the customer associated with the offer.

        Returns:
            dict: A dictionary with 'message' and 'status' keys indicating the status of the offer creation.

        """
        # Start with an empty query for car models
        car_models_query = DealershipCarModel.objects.filter(
            car_model=car_features.model,
            price__lte=max_price,
            count__gt=0
        )

        # Create a list to hold the Q objects for the optional car features
        optional_features_query = []

        # Build the Q objects for each optional car feature
        if car_features.color:
            optional_features_query.append(Q(car_model__features__color=car_features.color))
        if car_features.year:
            optional_features_query.append(Q(car_model__features__year=car_features.year))
        if car_features.mileage:
            optional_features_query.append(Q(car_model__features__mileage=car_features.mileage))
        if car_features.gearbox:
            optional_features_query.append(Q(car_model__features__gearbox=car_features.gearbox))
        if car_features.drive:
            optional_features_query.append(Q(car_model__features__drive=car_features.drive))
        if car_features.steering_wheel:
            optional_features_query.append(Q(car_model__features__steering_wheel=car_features.steering_wheel))
        if car_features.engine_power:
            optional_features_query.append(Q(car_model__features__engine_power=car_features.engine_power))
        if car_features.vin_number:
            optional_features_query.append(Q(car_model__features__vin_number=car_features.vin_number))

        # Combine the Q objects using OR operator
        if optional_features_query:
            car_models_query = car_models_query.filter(Q(*optional_features_query, _connector=Q.OR))

        # Choose the car model with the highest matching car features and the lowest price
        car_model_to_purchase = car_models_query.order_by('price').first()

        if car_model_to_purchase and car_model_to_purchase.car_model:
            # Update balances and create purchase history entry
            car_model_to_purchase.dealership.balance += car_model_to_purchase.price
            customer = Customer.objects.get(id=customer_id)
            customer.balance -= car_model_to_purchase.price
            car_model_to_purchase.count = F('count') - 1

            history_customer_dealership = CustomerDealershipHistory.objects.create(
                customer=customer,
                dealership=car_model_to_purchase.dealership,
                details=f"Car model {car_model_to_purchase.car_model} purchased for {car_model_to_purchase.price}"
            )

            car_model_to_purchase.dealership.sales_history.add(history_customer_dealership)
            customer.purchase_history.add(history_customer_dealership)

            car_model_to_purchase.dealership.save()
            customer.save()
            car_model_to_purchase.save()

            return {'message': 'Offer created successfully.', 'status': 'success'}
        return {'message': 'No matches found.', 'status': 'fail'}
