"""
Unit tests for the comments app.
"""
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post, Comment, CommentSettings
from .classifier import CommentClassifier


class PostModelTest(TestCase):
    """Test Post model."""
    
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post content."
        )
    
    def test_post_creation(self):
        """Test that a post can be created."""
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post content.")
        self.assertIsNotNone(self.post.created_at)
    
    def test_post_str(self):
        """Test Post string representation."""
        self.assertEqual(str(self.post), "Test Post")


class CommentModelTest(TestCase):
    """Test Comment model."""
    
    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content"
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author="Test User",
            content="This is a test comment."
        )
    
    def test_comment_creation(self):
        """Test that a comment can be created."""
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, "Test User")
        self.assertEqual(self.comment.content, "This is a test comment.")
        self.assertFalse(self.comment.flagged_for_review)
        self.assertIsNotNone(self.comment.created_at)
    
    def test_comment_str(self):
        """Test Comment string representation."""
        self.assertIn("Test User", str(self.comment))
        self.assertIn("This is a test comment", str(self.comment))


class CommentSettingsTest(TestCase):
    """Test CommentSettings model."""
    
    def test_singleton_behavior(self):
        """Test that CommentSettings is a singleton."""
        settings1 = CommentSettings.load()
        settings2 = CommentSettings.load()
        self.assertEqual(settings1.pk, settings2.pk)
        self.assertEqual(settings1.pk, 1)
    
    def test_default_enabled(self):
        """Test that comments are enabled by default."""
        settings = CommentSettings.load()
        self.assertTrue(settings.comments_enabled)


class CommentClassifierTest(TestCase):
    """Test CommentClassifier."""
    
    def test_rule_based_classification_spam_keywords(self):
        """Test rule-based classification detects spam keywords."""
        should_flag, reason = CommentClassifier.classify("This is a spam message", use_ml=False)
        self.assertTrue(should_flag)
        self.assertIn("suspicious keywords", reason)
    
    def test_rule_based_classification_profanity(self):
        """Test rule-based classification detects profanity."""
        should_flag, reason = CommentClassifier.classify("This is damn good", use_ml=False)
        self.assertTrue(should_flag)
        self.assertIn("profanity", reason.lower())
    
    def test_rule_based_classification_short_comment(self):
        """Test rule-based classification flags very short comments."""
        should_flag, reason = CommentClassifier.classify("Hi", use_ml=False)
        self.assertTrue(should_flag)
        self.assertIn("short", reason.lower())
    
    def test_rule_based_classification_long_comment(self):
        """Test rule-based classification flags very long comments."""
        long_text = "a" * 1001
        should_flag, reason = CommentClassifier.classify(long_text, use_ml=False)
        self.assertTrue(should_flag)
        self.assertIn("long", reason.lower())
    
    def test_rule_based_classification_normal_comment(self):
        """Test rule-based classification allows normal comments."""
        should_flag, reason = CommentClassifier.classify(
            "This is a normal, well-written comment with appropriate content.",
            use_ml=False
        )
        self.assertFalse(should_flag)
        self.assertIsNone(reason)
    
    def test_rule_based_classification_url(self):
        """Test rule-based classification detects URLs."""
        should_flag, reason = CommentClassifier.classify(
            "Check out https://example.com",
            use_ml=False
        )
        self.assertTrue(should_flag)
        self.assertIn("URL", reason)


class PostAPITest(TestCase):
    """Test Post API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content"
        )
    
    def test_list_posts(self):
        """Test listing posts."""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data or response.data)
    
    def test_get_post_detail(self):
        """Test getting a single post."""
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Post")
    
    def test_create_post(self):
        """Test creating a post."""
        data = {
            'title': 'New Post',
            'content': 'New post content'
        }
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)


class CommentAPITest(TestCase):
    """Test Comment API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content"
        )
        # Ensure comments are enabled
        settings = CommentSettings.load()
        settings.comments_enabled = True
        settings.save()
    
    def test_list_comments(self):
        """Test listing comments."""
        Comment.objects.create(
            post=self.post,
            author="Test User",
            content="Test comment"
        )
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_comment(self):
        """Test creating a comment."""
        data = {
            'post': self.post.id,
            'author': 'Test User',
            'content': 'This is a test comment'
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_create_comment_when_disabled(self):
        """Test that comments cannot be created when disabled."""
        settings = CommentSettings.load()
        settings.comments_enabled = False
        settings.save()
        
        data = {
            'post': self.post.id,
            'author': 'Test User',
            'content': 'This should fail'
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_flagged_comments(self):
        """Test getting flagged comments."""
        comment = Comment.objects.create(
            post=self.post,
            author="Test User",
            content="Test comment",
            flagged_for_review=True,
            flag_reason="Test reason"
        )
        response = self.client.get('/api/comments/flagged/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_comment_settings(self):
        """Test getting comment settings."""
        response = self.client.get('/api/comments/settings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('comments_enabled', response.data)


class CommentClassificationIntegrationTest(TestCase):
    """Integration tests for comment classification."""
    
    def setUp(self):
        self.client = APIClient()
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content"
        )
        settings = CommentSettings.load()
        settings.comments_enabled = True
        settings.save()
    
    def test_comment_auto_flagging_spam(self):
        """Test that spam comments are automatically flagged."""
        data = {
            'post': self.post.id,
            'author': 'Test User',
            'content': 'This is a spam message'
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        comment = Comment.objects.get(id=response.data['id'])
        self.assertTrue(comment.flagged_for_review)
        self.assertIsNotNone(comment.flag_reason)
    
    def test_comment_with_ml_classification(self):
        """Test comment creation with ML classification."""
        data = {
            'post': self.post.id,
            'author': 'Test User',
            'content': 'This is a normal comment'
        }
        response = self.client.post(
            '/api/comments/?use_ml=true&classifier_type=huggingface',
            data,
            format='json'
        )
        # Should succeed (may or may not flag depending on ML model)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
