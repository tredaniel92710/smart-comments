from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Post, Comment, CommentSettings
from .serializers import PostSerializer, CommentSerializer
from .classifier import CommentClassifier


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        flagged_only = self.request.query_params.get('flagged', None)
        
        if flagged_only == 'true':
            queryset = queryset.filter(flagged_for_review=True)
        
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        return queryset
    
    def perform_create(self, serializer):
        # Check if comments are enabled
        settings = CommentSettings.load()
        if not settings.comments_enabled:
            raise PermissionDenied("Comments are currently disabled. Please try again later.")
        
        comment = serializer.save()
        
        # Classify the comment
        use_ml = self.request.query_params.get('use_ml', 'false').lower() == 'true'
        classifier_type = self.request.query_params.get('classifier_type', None)  # 'huggingface' or 'openai'
        
        try:
            should_flag, reason = CommentClassifier.classify(
                comment.content, 
                use_ml=use_ml,
                classifier_type=classifier_type
            )
            
            if should_flag:
                comment.flagged_for_review = True
                comment.flag_reason = reason
                comment.save()
        except (ValueError, ImportError, Exception) as e:
            # If classification fails (e.g., OpenAI not configured), raise a validation error
            raise ValidationError(f"Classification failed: {str(e)}")
    
    @action(detail=False, methods=['get'])
    def flagged(self, request):
        """Get all flagged comments."""
        flagged_comments = Comment.objects.filter(flagged_for_review=True)
        serializer = self.get_serializer(flagged_comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='settings')
    def comment_settings(self, request):
        """Get comment settings (whether comments are enabled)."""
        settings = CommentSettings.load()
        return Response({
            'comments_enabled': settings.comments_enabled
        })
