from rest_framework import serializers
from .models import VehicleLocation


class VehicleLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleLocation
		fields = ['id', 'trip', 'latitude', 'longitude', 'heading_degrees', 'speed_kmph', 'timestamp']