"""
Classification service for comments.
Supports rule-based, Hugging Face pipeline, and OpenAI API classification.
"""
import re
import os
from typing import Tuple, Optional
from django.conf import settings


class CommentClassifier:
    """
    Classifier for flagging comments that need review.
    Supports multiple classification methods:
    - Rule-based (default)
    - Hugging Face transformers pipeline
    - OpenAI API
    """
    
    # Rule-based patterns for flagging
    FLAG_PATTERNS = [
        (r'\b(spam|scam|fake|fraud)\b', 'Contains suspicious keywords'),
        (r'\b(f\*ck|sh\*t|damn|hell)\b', 'Contains profanity'),
        (r'[!]{3,}', 'Excessive exclamation marks'),
        (r'[A-Z]{10,}', 'Excessive capitalization'),
        (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'Contains URL'),
        (r'[0-9]{4,}', 'Contains suspicious numbers'),
    ]
    
    # ML model cache (optional - can be loaded if transformers is available)
    _hf_model = None
    _openai_client = None
    
    @classmethod
    def classify(cls, comment_text: str, use_ml: bool = False, classifier_type: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Classify a comment and determine if it should be flagged for review.
        
        Args:
            comment_text: The text content of the comment
            use_ml: Whether to use ML model (if available) instead of rules
            classifier_type: Override default classifier type ('rules', 'huggingface', 'openai')
            
        Returns:
            Tuple of (should_flag, reason)
        """
        if not use_ml:
            return cls._classify_rules(comment_text)
        
        # Determine which classifier to use
        classifier = classifier_type or getattr(settings, 'CLASSIFIER_TYPE', 'rules')
        
        if classifier == 'openai':
            return cls._classify_openai(comment_text)
        elif classifier == 'huggingface':
            return cls._classify_huggingface(comment_text)
        else:
            # Fallback to rules if ML is requested but type is invalid
            return cls._classify_rules(comment_text)
    
    @classmethod
    def _classify_rules(cls, comment_text: str) -> Tuple[bool, Optional[str]]:
        """
        Rule-based classification using pattern matching.
        """
        comment_lower = comment_text.lower()
        
        for pattern, reason in cls.FLAG_PATTERNS:
            if re.search(pattern, comment_text, re.IGNORECASE):
                return True, reason
        
        # Check for very short comments (potential spam)
        if len(comment_text.strip()) < 5:
            return True, 'Very short comment'
        
        # Check for very long comments (potential spam)
        if len(comment_text) > 1000:
            return True, 'Very long comment'
        
        return False, None
    
    @classmethod
    def _classify_huggingface(cls, comment_text: str) -> Tuple[bool, Optional[str]]:
        """
        ML-based classification using Hugging Face transformers pipeline.
        """
        try:
            if cls._hf_model is None:
                from transformers import pipeline
                model_name = getattr(settings, 'HUGGINGFACE_MODEL', 'j-hartmann/emotion-english-distilroberta-base')
                cls._hf_model = pipeline(
                    "text-classification",
                    model=model_name,
                    return_all_scores=True
                )
            
            # Use ML model to detect negative emotions or toxicity
            results = cls._hf_model(comment_text)
            
            # Check for negative emotions or high toxicity scores
            for result in results[0]:
                label = result['label'].lower()
                score = result['score']
                
                # Check for negative emotions
                if label in ['anger', 'fear', 'sadness'] and score > 0.5:
                    return True, f'Detected {label} emotion (score: {score:.2f})'
                
                # Check for toxicity labels (common in toxicity models)
                if label in ['toxic', 'hate', 'spam', 'offensive'] and score > 0.5:
                    return True, f'Detected {label} content (score: {score:.2f})'
            
            return False, None
            
        except ImportError:
            # Fallback to rule-based if transformers not available
            return cls._classify_rules(comment_text)
        except Exception as e:
            # Fallback to rule-based if ML fails
            print(f"Hugging Face classification error: {e}")
            return cls._classify_rules(comment_text)
    
    @classmethod
    def _classify_openai(cls, comment_text: str) -> Tuple[bool, Optional[str]]:
        """
        ML-based classification using OpenAI API.
        """
        try:
            if cls._openai_client is None:
                from openai import OpenAI
                api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))
                if not api_key:
                    raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment variables or Django settings.")
                cls._openai_client = OpenAI(api_key=api_key)
            
            model = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
            
            # Create a prompt for classification
            prompt = f"""Analyze the following comment and determine if it should be flagged for review.
Consider factors like: spam, profanity, hate speech, toxicity, inappropriate content, or suspicious patterns.

Comment: "{comment_text}"

Respond in JSON format with:
- "should_flag": true/false
- "reason": brief explanation (if should_flag is true, otherwise null)
- "confidence": 0.0 to 1.0

Only respond with valid JSON, no additional text."""

            response = cls._openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a content moderation assistant. Analyze comments and determine if they need review."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            # Parse the response
            response_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            import json
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            result = json.loads(response_text)
            
            should_flag = result.get('should_flag', False)
            reason = result.get('reason', None)
            confidence = result.get('confidence', 0.0)
            
            if should_flag:
                return True, f"{reason} (confidence: {confidence:.2f})"
            else:
                return False, None
                
        except ImportError:
            # Raise error if openai library is not installed
            raise ImportError("OpenAI library is not installed. Please install it with: pip install openai")
        except ValueError as e:
            # Re-raise ValueError (e.g., API key not configured) so it can be shown to user
            raise
        except Exception as e:
            # For other errors, raise them so the user knows what went wrong
            error_msg = f"OpenAI classification error: {str(e)}"
            raise Exception(error_msg) from e
    
    @classmethod
    def load_ml_model(cls, classifier_type: Optional[str] = None):
        """Pre-load ML model for faster inference."""
        classifier = classifier_type or getattr(settings, 'CLASSIFIER_TYPE', 'rules')
        
        if classifier == 'huggingface':
            try:
                from transformers import pipeline
                model_name = getattr(settings, 'HUGGINGFACE_MODEL', 'j-hartmann/emotion-english-distilroberta-base')
                cls._hf_model = pipeline(
                    "text-classification",
                    model=model_name
                )
                print(f"Loaded Hugging Face model: {model_name}")
            except ImportError:
                print("Transformers library not available. Using rule-based classification only.")
            except Exception as e:
                print(f"Error loading Hugging Face model: {e}")
        
        elif classifier == 'openai':
            try:
                from openai import OpenAI
                api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))
                if api_key:
                    cls._openai_client = OpenAI(api_key=api_key)
                    model = getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo')
                    print(f"OpenAI client initialized with model: {model}")
                else:
                    print("OpenAI API key not configured.")
            except ImportError:
                print("OpenAI library not available. Using rule-based classification only.")
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
