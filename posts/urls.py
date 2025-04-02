from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserListCreate, PostListCreate, LikeViewSet, CommentViewSet, register, LikeCreateView, DislikeViewSet

# ✅ Instantiate the router
router = DefaultRouter()

# ✅ Register the viewsets with the router
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'dislikes', DislikeViewSet, basename='dislike')


urlpatterns = [
    # ✅ User Endpoints
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('register/', register, name='register'),

    # ✅ Post Endpoints
    path('posts/', PostListCreate.as_view(), name='post-list-create'),

    # ✅ Authentication
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # ✅ Include the router for GET requests on likes/comments
    path('api/', include(router.urls)),

    # ✅ Create a like
    path('likes/create/', LikeCreateView.as_view(), name='like-create'),

    path('', include(router.urls)),

]