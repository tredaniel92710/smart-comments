from django.apps import AppConfig
import sys


class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
    
    def ready(self):
        """Apply Python 3.14 compatibility patch when app is ready."""
        if sys.version_info >= (3, 14):
            from rest_framework.settings import api_settings
            
            # Patch the methods that access self.settings directly
            try:
                from rest_framework import views
                
                # Store original methods
                original_get_format_suffix = views.APIView.get_format_suffix
                original_get_exception_handler = views.APIView.get_exception_handler
                
                # Create patched versions that use api_settings directly
                def patched_get_format_suffix(self, **kwargs):
                    if api_settings.FORMAT_SUFFIX_KWARG:
                        return kwargs.get(api_settings.FORMAT_SUFFIX_KWARG)
                    return None
                
                def patched_get_exception_handler(self):
                    return api_settings.EXCEPTION_HANDLER
                
                # Replace the methods
                views.APIView.get_format_suffix = patched_get_format_suffix
                views.APIView.get_exception_handler = patched_get_exception_handler
                
                # Also patch any other methods that access self.settings
                # Patch get_view_name and get_view_description if they use self.settings
                if hasattr(views.APIView, 'get_view_name'):
                    original_get_view_name = views.APIView.get_view_name
                    def patched_get_view_name(self):
                        func = api_settings.VIEW_NAME_FUNCTION
                        if isinstance(func, str):
                            from django.utils.module_loading import import_string
                            func = import_string(func)
                        return func(self)
                    views.APIView.get_view_name = patched_get_view_name
                
                if hasattr(views.APIView, 'get_view_description'):
                    original_get_view_description = views.APIView.get_view_description
                    def patched_get_view_description(self, html=False):
                        func = api_settings.VIEW_DESCRIPTION_FUNCTION
                        if isinstance(func, str):
                            from django.utils.module_loading import import_string
                            func = import_string(func)
                        return func(self, html)
                    views.APIView.get_view_description = patched_get_view_description
                
            except (ImportError, AttributeError) as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to apply Python 3.14 compatibility patch: {e}")
