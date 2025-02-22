from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from posts.models import Post

class PostDetailViewTest(TestCase):
    
    def setUp(self):
        # Create a user and a post
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(content="Test post content", author=self.user)
        self.client = APIClient()

    def test_get_post_detail_authenticated_user(self):
        # Authenticate the user
        self.client.login(username='testuser', password='password')

        # Make a GET request to the post detail endpoint
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))

        # Check that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_detail_unauthenticated_user(self):
        # Make a GET request to the post detail endpoint without logging in
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))

        # Check that the response is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_post_detail_author(self):
        # Authenticate the user
        self.client.login(username='testuser', password='password')

        # Make a PUT request to update the post content
        response = self.client.put(reverse('post-detail', kwargs={'pk': self.post.pk}), data={'content': 'Updated post content'})

        # Check that the post content is updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated post content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_post_detail_non_author(self):
        # Create another user who is not the author of the post
        other_user = User.objects.create_user(username='otheruser', password='password')

        # Authenticate the other user
        self.client.login(username='otheruser', password='password')

        # Try to update the post content
        response = self.client.put(reverse('post-detail', kwargs={'pk': self.post.pk}), data={'content': 'Attempted update by non-author'})

        # Check that the response is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

