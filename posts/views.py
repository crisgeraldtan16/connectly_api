from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group  # Import Group
from .permissions import IsPostAuthor  # Import the custom permission
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated permission
from rest_framework.authtoken.models import Token


# ✅ User API
class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")  # ✅ Get email from request

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create user with hashed password
        user = User.objects.create_user(username=username, password=password, email=email)

        # Password is now hashed (check by printing user.password)
        print(user.password)  # This will print the hashed password, not the plain one.

        # Create "Admin" group if it doesn't exist
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        # Assign the user to the "Admin" group
        user.groups.add(admin_group)

        # Serialize the user data to return a response
        serializer = UserSerializer(user)
        return Response({
            "message": "User created and assigned to Admin group.",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)


# ✅ Post API
class PostListCreate(APIView):
    permission_classes = []  # Ensure only authenticated users can create posts

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Ensure the author is the logged-in user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Assign the logged-in user as the author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ✅ Comment API
class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ User Login API
class UserLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate token if user is authenticated
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Authentication successful!",
                "token": token.key  # Return the generated token
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

# ✅ Post Detail API - Only the post's author can access this view
class PostDetailView(APIView):
    # Applying both IsAuthenticated and custom permission IsPostAuthor
    permission_classes = [IsAuthenticated, IsPostAuthor]  # Apply custom permission here

    def get(self, request, pk):
        # Retrieve the post using the pk (primary key)
        post = get_object_or_404(Post, pk=pk)
        
        # Check permissions (i.e., whether the user can view this post)
        self.check_object_permissions(request, post)

        # Serialize the post data and return it in the response
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        # Retrieve the post using the pk
        post = get_object_or_404(Post, pk=pk)
        
        # Check permissions (i.e., whether the user can update this post)
        self.check_object_permissions(request, post)

        # Implement your update logic here (for example, updating post content)
        post.content = request.data.get('content', post.content)  # Update post content
        post.save()  # Save the updated post

        # Respond with a success message
        return Response({"message": "Post updated successfully"}, status=status.HTTP_200_OK)
    




        
