from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, authentication, permissions
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminRole
from .serializers import RideSerializer
from core.models import Ride

@extend_schema_view(
    list=extend_schema(tags=['rides']),
    create=extend_schema(tags=['rides']),
    retrieve=extend_schema(tags=['rides']),
    update=extend_schema(tags=['rides']),
    partial_update=extend_schema(tags=['rides']),
    destroy=extend_schema(tags=['rides']),
)
class RideViewSet(viewsets.ModelViewSet):
    """ViewSet for managing rides."""
    serializer_class = RideSerializer
    queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('events')
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    pagination_class = PageNumberPagination