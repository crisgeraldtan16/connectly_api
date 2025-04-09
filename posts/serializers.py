from rest_framework import serializers
from .models import Dislike, User, Post, Comment, Like

# ✅ Like serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

# ✅ Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Allow user as ID
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Allow post as ID

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at']

# ✅ User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']  # Change 'created_at' to 'date_joined'

# ✅ Dislike serializer
class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id', 'user', 'post', 'created_at']

# ✅ Serializer for the Post model, including comments and likes
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    dislikes = DislikeSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'privacy', 'comments', 'likes', 'dislikes', 'like_count', 'dislike_count']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()

    def to_representation(self, instance):
        # Get the current logged-in user from the context
        user = self.context.get('request').user

        # If it's a private post and the current user is not the author, return an empty dict
        if instance.privacy == 'private' and instance.author != user:
            return {}

        # Otherwise, serialize the instance normally
        return super().to_representation(instance)
