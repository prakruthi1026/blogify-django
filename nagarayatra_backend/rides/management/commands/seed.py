from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from rides.models import Route, DriverProfile, Trip
from datetime import timedelta


class Command(BaseCommand):
	help = 'Seed initial demo data for NagaraYatra'

	def handle(self, *args, **options):
		if not User.objects.filter(username='demo').exists():
			user = User.objects.create_user('demo', password='demo123')
			self.stdout.write('Created user demo/demo123')
		else:
			user = User.objects.get(username='demo')

		if not User.objects.filter(username='driver1').exists():
			driver_user = User.objects.create_user('driver1', password='driver123')
			DriverProfile.objects.create(user=driver_user, vehicle_reg_number='MH12AB1234', capacity=12)
			self.stdout.write('Created driver driver1/driver123')
		else:
			driver_user = User.objects.get(username='driver1')
			DriverProfile.objects.get_or_create(user=driver_user, defaults={'vehicle_reg_number': 'MH12AB1234', 'capacity': 12})

		route, _ = Route.objects.get_or_create(
			name='Industrial Area Loop',
			defaults={
				'start_name': 'Akurdi Station',
				'end_name': 'Industrial Zone',
				'stops': [
					{'name': 'Akurdi Station', 'lat': 18.648, 'lng': 73.759},
					{'name': 'MIDC Gate', 'lat': 18.654, 'lng': 73.770},
					{'name': 'Industrial Zone', 'lat': 18.660, 'lng': 73.780},
				],
			}
		)

		driver_profile = DriverProfile.objects.get(user=driver_user)
		for i in range(3):
			Trip.objects.get_or_create(
				route=route,
				driver=driver_profile,
				departure_time=timezone.now() + timedelta(hours=i+1),
				defaults={
					'estimated_arrival_time': timezone.now() + timedelta(hours=i+2),
					'price': 20.0,
					'seats_total': driver_profile.capacity,
					'seats_available': driver_profile.capacity,
				}
			)

		self.stdout.write(self.style.SUCCESS('Seed data created'))