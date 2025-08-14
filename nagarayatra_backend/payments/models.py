from django.db import models


class Payment(models.Model):
	STATUS_CHOICES = (
		('pending', 'Pending'),
		('success', 'Success'),
		('failed', 'Failed'),
	)

	booking = models.OneToOneField('rides.Booking', on_delete=models.CASCADE, related_name='payment')
	provider = models.CharField(max_length=50, default='mock')
	amount = models.DecimalField(max_digits=8, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	transaction_id = models.CharField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"Payment {self.id} ({self.status})"
