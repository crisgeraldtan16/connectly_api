from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Function to get the default user (avoiding migration issues)
def get_default_user():
    return User.objects.first().id if User.objects.exists() else None  # Handle empty User table


class Post(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    content = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')  # Added privacy field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

    @classmethod
    def get_visible_posts(cls, user):
        """Get posts that are either public or private posts authored by the given user"""
        return cls.objects.filter(
            Q(privacy='public') | Q(privacy='private', author=user)
        )


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)  # Use default function here
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='dislikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate dislikes

    def __str__(self):
        return f"{self.user.username} disliked Post {self.post.id}"

@classmethod
def get_visible_posts(cls, user):
    return cls.objects.filter(
        models.Q(privacy='public') | models.Q(author=user)
    )
