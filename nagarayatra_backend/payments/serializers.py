from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = ['id', 'booking', 'provider', 'amount', 'status', 'transaction_id', 'created_at', 'updated_at']