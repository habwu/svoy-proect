from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):
    """
    Разрешение: доступ только для администраторов.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsManagerUser(BasePermission):
    """
    Разрешение: доступ только для менеджеров.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsTeacherUser(BasePermission):
    """
    Разрешение: доступ только для учителей.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher


class IsStudentUser(BasePermission):
    """
    Разрешение: доступ только для учеников.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_child


class IsReadOnly(BasePermission):
    """
    Разрешение: доступ только для чтения (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
