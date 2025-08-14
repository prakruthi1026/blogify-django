import uuid
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from rides.models import Booking


class PaymentViewSet(viewsets.ModelViewSet):
	queryset = Payment.objects.all().order_by('-created_at')
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated]

	@action(detail=False, methods=['post'])
	def initiate(self, request):
		booking_id = request.data.get('booking_id')
		provider = request.data.get('provider', 'mock')
		booking = Booking.objects.get(id=booking_id, user=request.user)
		if hasattr(booking, 'payment'):
			payment = booking.payment
		else:
			payment = Payment.objects.create(booking=booking, provider=provider, amount=booking.amount, status='pending')
		return Response(PaymentSerializer(payment).data)

	@action(detail=True, methods=['post'])
	def confirm(self, request, pk=None):
		payment = self.get_object()
		# mock confirmation
		payment.status = 'success'
		payment.transaction_id = str(uuid.uuid4())
		payment.save(update_fields=['status', 'transaction_id', 'updated_at'])
		booking = payment.booking
		booking.status = 'confirmed'
		booking.save(update_fields=['status'])
		return Response(PaymentSerializer(payment).data)

	@action(detail=True, methods=['post'])
	def fail(self, request, pk=None):
		payment = self.get_object()
		payment.status = 'failed'
		payment.transaction_id = str(uuid.uuid4())
		payment.save(update_fields=['status', 'transaction_id', 'updated_at'])
		return Response(PaymentSerializer(payment).data)
