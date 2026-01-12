"""
Additional view tests for the comments app.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post, Comment, CommentSettings


class CommentViewSetTest(TestCase):
    """Test CommentViewSet endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content"
        )
        settings = CommentSettings.load()
        settings.comments_enabled = True
        settings.save()
    
    def test_filter_comments_by_post(self):
        """Test filtering comments by post ID."""
        comment1 = Comment.objects.create(
            post=self.post,
            author="User 1",
            content="Comment 1"
        )
        post2 = Post.objects.create(title="Post 2", content="Content 2")
        comment2 = Comment.objects.create(
            post=post2,
            author="User 2",
            content="Comment 2"
        )
        
        response = self.client.get(f'/api/comments/?post={self.post.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], comment1.id)
    
    def test_filter_flagged_comments(self):
        """Test filtering flagged comments."""
        Comment.objects.create(
            post=self.post,
            author="User 1",
            content="Normal comment",
            flagged_for_review=False
        )
        flagged_comment = Comment.objects.create(
            post=self.post,
            author="User 2",
            content="Flagged comment",
            flagged_for_review=True,
            flag_reason="Test reason"
        )
        
        response = self.client.get('/api/comments/?flagged=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], flagged_comment.id)
    
    def test_comment_settings_endpoint(self):
        """Test comment settings endpoint."""
        response = self.client.get('/api/comments/settings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('comments_enabled', response.data)
        self.assertIsInstance(response.data['comments_enabled'], bool)
