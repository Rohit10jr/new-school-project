from rest_framework.permissions import BasePermission, IsAdminUser

class IsStaffUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and (request.user.user_type == 'is_staff') )
    

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and (request.user.user_type == 'is_admin'))