from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and hasattr(user, 'is_teacher') and user.is_teacher and user.is_active)


class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and hasattr(user, 'is_student') and user.is_student and user.is_active)


class IsTeacherOrStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated
                and user.is_active
                and (user.is_teacher or user.is_staff or user.is_superuser
                     )
        )


class IsStudentOrStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated
                and user.is_active
                and (user.is_student or user.is_staff or user.is_superuser
                     )
        )


class IsStaffOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated and
                user.is_active and
                (user.is_staff or user.is_superuser)
        )

