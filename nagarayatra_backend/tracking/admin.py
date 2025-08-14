from django.contrib import admin
from .models import VehicleLocation


@admin.register(VehicleLocation)
class VehicleLocationAdmin(admin.ModelAdmin):
	list_display = ('id', 'trip', 'latitude', 'longitude', 'speed_kmph', 'timestamp')
	list_filter = ('trip',)
