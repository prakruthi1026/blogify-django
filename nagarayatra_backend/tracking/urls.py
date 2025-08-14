from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleLocationViewSet

router = DefaultRouter()
router.register(r'locations', VehicleLocationViewSet)

urlpatterns = [
	path('', include(router.urls)),
]