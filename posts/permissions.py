from rest_framework.permissions import BasePermission

class IsPostAuthor(BasePermission):
    """
    Custom permission to only allow the author of a post to edit or view it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the author of the post is the current user
        return obj.author == request.user
