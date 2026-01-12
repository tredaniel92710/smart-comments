import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Post } from '../types';
import { postsApi, commentsApi } from '../services/api';
import CommentList from './CommentList';
import CommentForm from './CommentForm';
import './PostDetail.css';

const PostDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCommentForm, setShowCommentForm] = useState(false);
  const [commentsEnabled, setCommentsEnabled] = useState(true);

  useEffect(() => {
    if (id) {
      loadPost();
      loadCommentSettings();
    }
  }, [id]);

  const loadPost = async () => {
    if (!id) return;
    
    try {
      setLoading(true);
      const data = await postsApi.getById(parseInt(id));
      setPost(data);
      setError(null);
    } catch (err) {
      setError('Failed to load post');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadCommentSettings = async () => {
    try {
      const settings = await commentsApi.getSettings();
      setCommentsEnabled(settings.comments_enabled);
    } catch (error) {
      console.error('Failed to load comment settings:', error);
      setCommentsEnabled(true);
    }
  };

  const handleCommentSubmit = async (
    author: string,
    content: string,
    useMl: boolean,
    classifierType?: 'huggingface' | 'openai'
  ) => {
    if (!post) return;
    
    try {
      await commentsApi.create(post.id, author, content, useMl, classifierType);
      setShowCommentForm(false);
      await loadPost(); // Reload post to get updated comments
      toast.success('Comment added successfully!');
    } catch (error: any) {
      console.error('Failed to create comment:', error);
      let errorMessage = 'Failed to create comment. Please try again.';
      
      if (error.response?.data) {
        if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data.non_field_errors) {
          errorMessage = Array.isArray(error.response.data.non_field_errors)
            ? error.response.data.non_field_errors[0]
            : error.response.data.non_field_errors;
        } else if (typeof error.response.data === 'string') {
          errorMessage = error.response.data;
        } else if (error.response.data.message) {
          errorMessage = error.response.data.message;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast.error(errorMessage);
    }
  };

  if (loading) {
    return <div className="loading">Loading post...</div>;
  }

  if (error || !post) {
    return (
      <div className="error-container">
        <div className="error">{error || 'Post not found'}</div>
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Posts
        </button>
      </div>
    );
  }

  return (
    <div className="post-detail">
      <button className="back-button" onClick={() => navigate('/')}>
        ← Back to Posts
      </button>
      
      <article className="post-detail-content">
        <header className="post-detail-header">
          <h1 className="post-detail-title">{post.title}</h1>
          <div className="post-detail-meta">
            <span className="post-detail-date">
              {new Date(post.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </span>
            <span className="post-detail-comments-count">
              {post.comment_count} {post.comment_count === 1 ? 'comment' : 'comments'}
            </span>
          </div>
        </header>
        
        <div className="post-detail-body">
          <p>{post.content}</p>
        </div>
      </article>

      <section className="post-detail-comments">
        <div className="comments-section-header">
          <h2>Comments ({post.comment_count})</h2>
          {commentsEnabled && (
            <button
              className="add-comment-btn"
              onClick={() => setShowCommentForm(!showCommentForm)}
            >
              {showCommentForm ? 'Cancel' : 'Add Comment'}
            </button>
          )}
          {!commentsEnabled && (
            <span className="comments-disabled-message">
              Comments are currently disabled
            </span>
          )}
        </div>

        {showCommentForm && commentsEnabled && (
          <CommentForm onSubmit={handleCommentSubmit} />
        )}

        <CommentList comments={post.comments} />
      </section>
    </div>
  );
};

export default PostDetail;
