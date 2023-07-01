from django.urls import path, include
from rest_framework import routers

from .views import CarModelViewSet

router = routers.DefaultRouter()
router.register(r'car-models', CarModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]