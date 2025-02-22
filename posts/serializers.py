from rest_framework import serializers
from .models import User, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # ✅ Prevents direct assignment
    comments = serializers.StringRelatedField(many=True, read_only=True)  # ✅ Shows related comments

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # ✅ Prevents direct assignment
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # ✅ Ensures post exists

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def validate_post(self, value):
        """ Ensure the referenced post exists """
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value

