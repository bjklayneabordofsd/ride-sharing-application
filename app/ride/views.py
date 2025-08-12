from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RideSerializer
from .permissions import IsAdminRole
from core.models import Ride


@extend_schema_view(
    list=extend_schema(
        tags=['rides'],
        description="List all rides with optional filtering and sorting",
        parameters=[
            OpenApiParameter(
                name='status',
                description='Filter by ride status',
                required=False,
                type=str,
                enum=['en-route', 'pickup', 'dropoff']
            ),

            #GET /api/ride/rides/?status=pickup (filter by status)
            #GET /api/ride/rides/?id_rider__email=user@example.com (filter by email)

            OpenApiParameter(
                name='id_rider__email',
                description='Filter by rider email address',
                required=False,
                type=str,
            ),

            # GET /api/ride/rides/?ordering=pickup_time (sort ascending)
            # GET /api/ride/rides/?ordering=-pickup_time (sort descending)
            # GET /api/ride/rides/?status=pickup&ordering=-pickup_time (combine filters) 
            
            OpenApiParameter(
                name='ordering',
                description='Sort results by pickup_time. Use "-pickup_time" for descending order',
                required=False,
                type=str,
                enum=['pickup_time', '-pickup_time']
            ),
        ]
    ),
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

    """ViewSet for Filtering and Sorting"""
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'id_rider__email': ['exact'],
    }
    ordering_fields = ['pickup_time']
    ordering = ['-pickup_time'] 