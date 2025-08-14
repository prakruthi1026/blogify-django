from django.shortcuts import render
from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Route, Trip, Booking, DriverProfile, DemandEvent
from .serializers import RouteSerializer, TripSerializer, BookingSerializer, DemandEventSerializer


# Create your views here.


class AuthViewSet(viewsets.ViewSet):
	permission_classes = [AllowAny]

	@action(detail=False, methods=['post'])
	def register(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		if not username or not password:
			return Response({'detail': 'username and password required'}, status=400)
		if User.objects.filter(username=username).exists():
			return Response({'detail': 'username taken'}, status=400)
		user = User.objects.create_user(username=username, password=password)
		return Response({'id': user.id, 'username': user.username})

	@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
	def me(self, request):
		user = request.user
		profile = getattr(user, 'driver_profile', None)
		return Response({
			'id': user.id,
			'username': user.username,
			'is_driver': profile is not None,
			'driver': {
				'id': profile.id,
				'vehicle_reg_number': profile.vehicle_reg_number,
				'capacity': profile.capacity,
			} if profile else None
		})


class RouteViewSet(viewsets.ModelViewSet):
	queryset = Route.objects.filter(is_active=True).order_by('name')
	serializer_class = RouteSerializer
	permission_classes = [AllowAny]
	filterset_fields = ['start_name', 'end_name']
	search_fields = ['name', 'start_name', 'end_name']
	ordering_fields = ['name', 'created_at']


class TripViewSet(viewsets.ModelViewSet):
	queryset = Trip.objects.all().order_by('-departure_time')
	serializer_class = TripSerializer
	permission_classes = [AllowAny]
	filterset_fields = ['route', 'driver', 'status']
	ordering_fields = ['departure_time', 'price']

	@action(detail=False, methods=['get'])
	def upcoming(self, request):
		now = timezone.now()
		qs = self.get_queryset().filter(departure_time__gte=now, status='scheduled')
		page = self.paginate_queryset(qs)
		serializer = self.get_serializer(page or qs, many=True)
		if page is not None:
			return self.get_paginated_response(serializer.data)
		return Response(serializer.data)

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		# Only drivers can create trips
		if not request.user.is_authenticated or not hasattr(request.user, 'driver_profile'):
			return Response({'detail': 'Driver account required'}, status=403)
		route_id = request.data.get('route_id')
		departure_time = request.data.get('departure_time')
		price = request.data.get('price')
		route = Route.objects.get(id=route_id)
		driver = request.user.driver_profile
		trip = Trip.objects.create(
			route=route,
			driver=driver,
			departure_time=departure_time,
			price=price,
			seats_total=driver.capacity,
			seats_available=driver.capacity,
		)
		return Response(TripSerializer(trip).data, status=201)


class BookingViewSet(viewsets.ModelViewSet):
	queryset = Booking.objects.all().order_by('-created_at')
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated]

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		trip_id = request.data.get('trip_id')
		seats = int(request.data.get('seats', 1))
		trip = Trip.objects.select_for_update().get(id=trip_id)
		if trip.status != 'scheduled':
			return Response({'detail': 'Trip not open for booking'}, status=400)
		if seats <= 0 or seats > trip.seats_available:
			return Response({'detail': 'Invalid seat count'}, status=400)
		amount = float(trip.price) * seats
		trip.seats_available -= seats
		trip.save(update_fields=['seats_available'])
		booking = Booking.objects.create(user=request.user, trip=trip, seats=seats, amount=amount, status='pending')
		serializer = self.get_serializer(booking)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=['post'])
	def cancel(self, request, pk=None):
		booking = self.get_object()
		if booking.status == 'cancelled':
			return Response({'detail': 'Already cancelled'})
		booking.status = 'cancelled'
		booking.save(update_fields=['status'])
		trip = booking.trip
		trip.seats_available = min(trip.seats_total, trip.seats_available + booking.seats)
		trip.save(update_fields=['seats_available'])
		return Response({'detail': 'Cancelled'})


class DemandEventViewSet(viewsets.ModelViewSet):
	queryset = DemandEvent.objects.all().order_by('-timestamp')
	serializer_class = DemandEventSerializer
	permission_classes = [AllowAny]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

	@action(detail=False, methods=['get'])
	def clusters(self, request):
		# naive clustering by rounding lat/lng to 2 decimals
		from django.db.models import Count
		from django.db.models.functions import Round
		qs = DemandEvent.objects.all()
		clusters = qs.values('event_type').annotate(
			lat_bucket=Round('latitude', 2),
			lng_bucket=Round('longitude', 2),
			count=Count('id')
		).order_by('-count')[:50]
		return Response(list(clusters))
