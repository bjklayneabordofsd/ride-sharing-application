"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Ride, RideEvent

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id_user']
    list_display = ['email', 'first_name', 'last_name', 'role']
    list_filter = ['role', 'is_active', 'is_staff']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'first_name',
                    'last_name', 
                    'phone_number',
                    'role',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone_number',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
class RideEventInline(admin.TabularInline):
    model = RideEvent
    extra = 0
    readonly_fields = ('description', 'created_at')
    can_delete = False

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id_ride', 'status', 'id_rider', 'id_driver', 'pickup_time')
    list_filter = ('status',)
    inlines = [RideEventInline]


admin.site.register(models.User, UserAdmin)

