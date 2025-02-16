from django.urls import path
from .views import UserListCreate, PostListCreate, CommentListCreate
from .views import UserListCreate, UserLogin  # Import your views


urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),  # ✅ Register User API
    path('login/', UserLogin.as_view(), name='user-login'),  # ✅ Register Login API


]
