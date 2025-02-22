from django.urls import path
from .views import UserListCreate, PostListCreate, CommentListCreate
from .views import UserLogin, PostDetailView  # Import your views

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),  # ✅ Register User API
    path('posts/', PostListCreate.as_view(), name='post-list-create'),  # ✅ Register Post API
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),  # ✅ Register Comment API
    path('login/', UserLogin.as_view(), name='user-login'),  # ✅ Register Login API
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),# Use 'pk' for primary key
]

