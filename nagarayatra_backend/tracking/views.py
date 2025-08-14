from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import VehicleLocation
from .serializers import VehicleLocationSerializer


# Create your views here.

class VehicleLocationViewSet(viewsets.ModelViewSet):
	queryset = VehicleLocation.objects.all()
	serializer_class = VehicleLocationSerializer
	permission_classes = [AllowAny]
	filterset_fields = ['trip']
	ordering = ['-timestamp']

	@action(detail=False, methods=['get'])
	def latest(self, request):
		trip_id = request.query_params.get('trip_id')
		if not trip_id:
			return Response({'detail': 'trip_id required'}, status=400)
		obj = VehicleLocation.objects.filter(trip_id=trip_id).order_by('-timestamp').first()
		if not obj:
			return Response({'detail': 'Not found'}, status=404)
		return Response(self.get_serializer(obj).data)
