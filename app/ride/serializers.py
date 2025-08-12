from rest_framework import serializers
from core.models import Ride, RideEvent


class RideEventSerializer(serializers.ModelSerializer):
    """Serializer for RideEvent objects."""
    
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'id_ride', 'description', 'created_at']
        read_only_fields = fields


class RideSerializer(serializers.ModelSerializer):
    """Serializer for Ride objects."""
    events = RideEventSerializer(many=True, read_only=True)
    
    """
    Adding the events in this serializer prevents n+1 query problem
    """
    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider',
            'id_driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'events',  
        ]
        read_only_fields = ['id_ride']