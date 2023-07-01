from django.urls import path, include
from rest_framework import routers

from .views import AuthorizationViewSet

router = routers.DefaultRouter()
router.register(r'authorization', AuthorizationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]