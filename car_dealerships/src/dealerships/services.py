from django.db.models import F, Q

from src.transaction_history.models import DealershipSupplierHistory
from src.suppliers.models import SupplierCarModel
from .models import Dealership, DealershipCarModel


class CarPurchaseService:
    @staticmethod
    def purchase_cars():
        # Get all dealerships
        dealerships = Dealership.objects.all()

        for dealership in dealerships:
            # Get car features of the dealership
            car_features = dealership.car_features

            # Start with an empty query for car models
            car_models_query = SupplierCarModel.objects.all()

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
                # Update the dealership's balance and decrease the count
                # of the purchased car model in the supplier's stock
                dealership.balance -= car_model_to_purchase.price

                # Create the dealership-supplier history object
                history_dealership_supplier = DealershipSupplierHistory.objects.create(
                    dealership=dealership,
                    supplier=car_model_to_purchase.supplier,
                    details=f"Car model {car_model_to_purchase.car_model} purchased for {car_model_to_purchase.price}"
                )

                dealership.purchase_history.add(history_dealership_supplier)
                car_model_to_purchase.supplier.sales_history.add(history_dealership_supplier)

                try:
                    dealership_car_model = DealershipCarModel.objects.get(dealership=dealership,
                                                                          car_model=car_model_to_purchase.car_model)
                    dealership_car_model.count = F('count') + 1
                    dealership_car_model.save()
                except DealershipCarModel.DoesNotExist:
                    dealership_car_model = DealershipCarModel.objects.create(
                        dealership=dealership,
                        car_model=car_model_to_purchase.car_model,
                        price=car_model_to_purchase.price * 2,
                        count=1
                    )
                    dealership.dealershipcarmodel_set.add(dealership_car_model)

                dealership.save()
                car_model_to_purchase.save()
