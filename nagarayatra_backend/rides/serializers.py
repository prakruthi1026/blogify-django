from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Route, Trip, Booking, DriverProfile, DemandEvent


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name']


class DriverProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)

	class Meta:
		model = DriverProfile
		fields = ['id', 'user', 'vehicle_type', 'vehicle_reg_number', 'capacity', 'is_available']


class RouteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Route
		fields = ['id', 'name', 'start_name', 'end_name', 'stops', 'is_active']


class TripSerializer(serializers.ModelSerializer):
	route = RouteSerializer(read_only=True)
	driver = DriverProfileSerializer(read_only=True)

	class Meta:
		model = Trip
		fields = ['id', 'route', 'driver', 'departure_time', 'estimated_arrival_time', 'price', 'seats_total', 'seats_available', 'status']


class BookingSerializer(serializers.ModelSerializer):
	trip = TripSerializer(read_only=True)

	class Meta:
		model = Booking
		fields = ['id', 'trip', 'seats', 'amount', 'status', 'created_at']


class DemandEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = DemandEvent
		fields = ['id', 'user', 'latitude', 'longitude', 'event_type', 'timestamp', 'meta']