from rest_framework.permissions import BasePermission

class IsPostAuthor(BasePermission):
    """
    Custom permission to allow only the author of a post to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user  # Ensure the request user is the post author
