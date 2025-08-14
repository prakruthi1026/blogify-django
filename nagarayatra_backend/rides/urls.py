from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, TripViewSet, BookingViewSet, DemandEventViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'trips', TripViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'demand', DemandEventViewSet)
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
	path('', include(router.urls)),
]