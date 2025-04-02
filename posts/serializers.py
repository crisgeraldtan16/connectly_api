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
    dislikes = DislikeSerializer(many=True, read_only=True)  # Include dislikes
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()  # Add dislike count

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments', 'likes', 'dislikes', 'like_count', 'dislike_count']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()  # Count dislikes
