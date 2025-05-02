from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and hasattr(user, 'is_staff') and user.is_staff and user.is_active)

class IsTeacherUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and hasattr(user, 'is_teacher') and user.is_teacher and user.is_active)

class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and hasattr(user, 'is_student') and user.is_student and user.is_active)
