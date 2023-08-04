from rest_framework import permissions

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_teacher)

class IsNormalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not (request.user.is_staff or request.user.is_teacher)
