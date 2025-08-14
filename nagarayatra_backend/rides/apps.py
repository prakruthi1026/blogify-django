from django.apps import AppConfig


class RidesConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'rides'
	singular_verbose_name = 'Ride'
	verbose_name = 'Rides'
