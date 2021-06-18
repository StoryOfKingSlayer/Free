from rest_framework import permissions

class IsAdminOrManager(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user.role == "Meneger" or user.role == "Admin"):
            return False
        return True