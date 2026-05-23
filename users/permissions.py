from rest_framework import permissions


class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение (GET, HEAD, OPTIONS) всем авторизованным пользователям,
    а изменение (POST, PUT, PATCH, DELETE) — только пользователям со статусом библиотекаря или суперпользователя.
    """

    def has_permission(self, request, view):
        # Проверяем, авторизован ли пользователь
        if not (request.user and request.user.is_authenticated):
            return False

        # Если это безопасный метод чтения (GET) — пускаем всех авторизованных
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для изменения данных (POST, PUT и т.д.) делаем проверку
        return bool(request.user.is_librarian or request.user.is_superuser)
