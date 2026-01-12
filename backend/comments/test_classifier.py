"""
Additional classifier tests.
"""
from django.test import TestCase
from .classifier import CommentClassifier


class CommentClassifierAdvancedTest(TestCase):
    """Advanced tests for CommentClassifier."""
    
    def test_excessive_capitalization(self):
        """Test detection of excessive capitalization."""
        should_flag, reason = CommentClassifier.classify(
            "THIS IS ALL CAPS AND SHOULD BE FLAGGED",
            use_ml=False
        )
        self.assertTrue(should_flag)
        self.assertIn("capitalization", reason.lower())
    
    def test_excessive_exclamation(self):
        """Test detection of excessive exclamation marks."""
        should_flag, reason = CommentClassifier.classify(
            "This is exciting!!!",
            use_ml=False
        )
        self.assertTrue(should_flag)
        self.assertIn("exclamation", reason.lower())
    
    def test_suspicious_numbers(self):
        """Test detection of suspicious number patterns."""
        should_flag, reason = CommentClassifier.classify(
            "Call me at 1234567890",
            use_ml=False
        )
        self.assertTrue(should_flag)
        self.assertIn("numbers", reason.lower())
    
    def test_normal_comment_passes(self):
        """Test that normal comments pass classification."""
        should_flag, reason = CommentClassifier.classify(
            "This is a well-written, thoughtful comment that should not be flagged.",
            use_ml=False
        )
        self.assertFalse(should_flag)
        self.assertIsNone(reason)
    
    def test_classifier_type_override(self):
        """Test that classifier_type parameter works."""
        # This should use rules even if use_ml is True but classifier_type is not set
        should_flag, reason = CommentClassifier.classify(
            "This is spam",
            use_ml=True,
            classifier_type='rules'
        )
        self.assertTrue(should_flag)
