from django.contrib import admin
from .models import Route, DriverProfile, Trip, Booking, DemandEvent


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'start_name', 'end_name', 'is_active')
	search_fields = ('name', 'start_name', 'end_name')


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'vehicle_reg_number', 'capacity', 'is_available')
	search_fields = ('user__username', 'vehicle_reg_number')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
	list_display = ('id', 'route', 'driver', 'departure_time', 'price', 'seats_available', 'status')
	list_filter = ('status', 'route')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'trip', 'seats', 'amount', 'status', 'created_at')
	list_filter = ('status',)


@admin.register(DemandEvent)
class DemandEventAdmin(admin.ModelAdmin):
	list_display = ('id', 'event_type', 'latitude', 'longitude', 'timestamp', 'user')
	list_filter = ('event_type',)
