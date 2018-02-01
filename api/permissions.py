from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a posts and owners of accounts
    to manipulate them (and also admins of course).
    """
    def has_object_permission(self, request, view, obj):
        # always allow GET and admins
        if request.method in permissions.SAFE_METHODS or \
                request.user.is_superuser and request.user.is_staff:
            return True

        # If it has author, it is a post
        if hasattr(obj, 'author'):
            return obj.author == request.user
        # Else it's a user
        else:
            return obj == request.user
