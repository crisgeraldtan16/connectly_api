from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from posts.permissions import IsPostAuthor
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer
from django.contrib.auth.models import User 
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth.models import Group, User

from rest_framework import permissions
from .models import Like, Comment, Dislike
from .serializers import LikeSerializer, CommentSerializer, DislikeSerializer


# ✅ Create an Admin group and assign a user to it
admin_group, created = Group.objects.get_or_create(name="Admin")

try:
    user = User.objects.get(username="testuser01")  # Replace with actual admin username
    user.groups.add(admin_group)
    print(f"User {user.username} added to Admin group")
except User.DoesNotExist:
    print("User does not exist")

# ✅ Register API
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        # Create user with encrypted password
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)

# ✅ User API
class UserListCreate(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view
    authentication_classes = [TokenAuthentication]  # Token authentication required for this view

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Post API
class PostListCreate(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create posts
    authentication_classes = [TokenAuthentication]  # Ensure that token is required to authenticate users

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # The logged-in user is assigned as the author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Post Detail API
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]  # Require authentication & author check
    authentication_classes = [TokenAuthentication]  # Token authentication required for this view

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)  # Enforce permissions
        return Response({"content": post.content})
    
# ✅ Like API (ViewSet)
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Ensure that a user can't like the same post more than once
        post_id = request.data.get("post")
        post = get_object_or_404(Post, pk=post_id)
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the like
        return super().create(request, *args, **kwargs)

# ✅ Comment API (ViewSet)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    
# ✅ Like Create API (Function-Based View)
class LikeCreateAPIView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)

# ✅ Like Create API (Class-Based View)
class LikeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ✅ Dislike API (ViewSet)
class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        post = get_object_or_404(Post, pk=post_id)

        # Prevent duplicate dislikes
        if Dislike.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already disliked this post."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)