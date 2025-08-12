from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ride, RideEvent


@receiver(pre_save, sender=Ride)
def track_ride_changes(sender, instance, **kwargs):
    """Store old values before save."""
    if instance.pk:
        try:
            instance._old_status = Ride.objects.get(pk=instance.pk).status
        except Ride.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Ride)
def create_ride_event(sender, instance, created, **kwargs):
    """Create RideEvent entries when Ride is created or updated."""
    
    if created:
        RideEvent.objects.create(
            id_ride=instance,
            description=f"Ride created with status '{instance.status}'"
        )
    else:
        # Check if status changed
        if hasattr(instance, '_old_status') and instance._old_status != instance.status:
            RideEvent.objects.create(
                id_ride=instance,
                description=f"Status changed from '{instance._old_status}' to '{instance.status}'"
            )