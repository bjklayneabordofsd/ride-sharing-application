"""
URL mappings for the ride API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('rides', views.RideViewSet)

app_name = 'ride'

urlpatterns = [
    path('', include(router.urls)),
]