from django.urls import path, include
from rest_framework import routers

from .views import DealershipViewSet

router = routers.DefaultRouter()
router.register(r'dealerships', DealershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]