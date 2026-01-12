from django.contrib import admin
from .models import Post, Comment, CommentSettings


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'flagged_for_review', 'flag_reason']
    list_filter = ['flagged_for_review', 'created_at']
    search_fields = ['author', 'content']


@admin.register(CommentSettings)
class CommentSettingsAdmin(admin.ModelAdmin):
    list_display = ['comments_enabled']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not CommentSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the singleton
        return False
