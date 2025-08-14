from django.conf import settings
from django.db import models


class Route(models.Model):
	name = models.CharField(max_length=120)
	start_name = models.CharField(max_length=120)
	end_name = models.CharField(max_length=120)
	stops = models.JSONField(default=list, blank=True)  # list of {name, lat, lng}
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.name


class DriverProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
	vehicle_type = models.CharField(max_length=50, default='tempo')
	vehicle_reg_number = models.CharField(max_length=50)
	capacity = models.PositiveIntegerField(default=10)
	is_available = models.BooleanField(default=True)

	def __str__(self) -> str:
		return f"Driver {self.user.username} ({self.vehicle_reg_number})"


class Trip(models.Model):
	STATUS_CHOICES = (
		('scheduled', 'Scheduled'),
		('ongoing', 'Ongoing'),
		('completed', 'Completed'),
		('cancelled', 'Cancelled'),
	)

	route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
	driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='trips')
	departure_time = models.DateTimeField()
	estimated_arrival_time = models.DateTimeField(null=True, blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	seats_total = models.PositiveIntegerField(default=10)
	seats_available = models.PositiveIntegerField(default=10)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Trip {self.id} - {self.route.name}"


class Booking(models.Model):
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('confirmed', 'Confirmed'),
		('cancelled', 'Cancelled'),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
	trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
	seats = models.PositiveIntegerField(default=1)
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Booking {self.id} - {self.user.username} - {self.trip_id}"


class DemandEvent(models.Model):
	EVENT_CHOICES = (
		('view', 'View'),
		('search', 'Search'),
		('booking', 'Booking'),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='demand_events')
	latitude = models.FloatField()
	longitude = models.FloatField()
	event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
	timestamp = models.DateTimeField(auto_now_add=True)
	meta = models.JSONField(default=dict, blank=True)

	def __str__(self) -> str:
		return f"Demand {self.event_type} @ {self.latitude},{self.longitude}"
