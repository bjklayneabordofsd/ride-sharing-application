from rest_framework import viewsets, authentication, permissions
from .serializers import RideSerializer
from core.models import Ride


class RideViewSet(viewsets.ModelViewSet):
    """ViewSet for managing rides."""
    serializer_class = RideSerializer
    queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('events')
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]