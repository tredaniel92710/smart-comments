from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    flagged_for_review = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author}: {self.content[:50]}"


class CommentSettings(models.Model):
    """
    Singleton model to store comment system settings.
    Only one instance should exist.
    """
    comments_enabled = models.BooleanField(default=True, help_text="Allow users to add new comments")
    
    class Meta:
        verbose_name = "Comment Settings"
        verbose_name_plural = "Comment Settings"
    
    def __str__(self):
        return "Comment Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
