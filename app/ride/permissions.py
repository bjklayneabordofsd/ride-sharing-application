from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """Allow access only to users with 'admin' role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'