from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("user is not authenticated")
        if not request.user.role =="seller":
            raise PermissionDenied("user is not a seller")
        return True
    

