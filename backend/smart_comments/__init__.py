"""
Python 3.14 compatibility patch for Django REST Framework.
This fixes the issue where self.settings is treated as a function instead of an object.

The actual patch is applied in comments.apps.CommentsConfig.ready() to ensure
Django settings are configured before patching.
"""
