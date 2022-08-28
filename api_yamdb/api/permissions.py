from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return (request.user.role == 'admin'
                    or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        else:
            return (request.user.role == 'admin'
                    or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser
            )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
