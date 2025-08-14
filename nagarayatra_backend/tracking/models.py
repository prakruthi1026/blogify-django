from django.db import models

# Create your models here.


class VehicleLocation(models.Model):
	trip = models.ForeignKey('rides.Trip', on_delete=models.CASCADE, related_name='locations')
	latitude = models.FloatField()
	longitude = models.FloatField()
	heading_degrees = models.FloatField(default=0.0)
	speed_kmph = models.FloatField(default=0.0)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self) -> str:
		return f"Trip {self.trip_id} @ {self.latitude},{self.longitude}"
