import React, { useState } from 'react';
import { toast } from 'react-toastify';
import { Post } from '../types';
import { commentsApi } from '../services/api';
import CommentList from './CommentList';
import CommentForm from './CommentForm';
import './PostCard.css';

interface PostCardProps {
  post: Post;
  onCommentAdded: (postId: number) => void;
  commentsEnabled: boolean;
}

const PostCard: React.FC<PostCardProps> = ({ post, onCommentAdded, commentsEnabled }) => {
  const [showCommentForm, setShowCommentForm] = useState(false);

  const handleCommentSubmit = async (author: string, content: string, useMl: boolean, classifierType?: 'huggingface' | 'openai') => {
    try {
      await commentsApi.create(post.id, author, content, useMl, classifierType);
      setShowCommentForm(false);
      onCommentAdded(post.id);
      toast.success('Comment added successfully!');
    } catch (error: any) {
      console.error('Failed to create comment:', error);
      // Try to extract error message from various possible locations
      let errorMessage = 'Failed to create comment. Please try again.';
      
      if (error.response?.data) {
        // Check for detail field (DRF standard)
        if (error.response.data.detail) {
          errorMessage = error.response.data.detail;
        }
        // Check for non_field_errors (DRF validation errors)
        else if (error.response.data.non_field_errors) {
          errorMessage = Array.isArray(error.response.data.non_field_errors) 
            ? error.response.data.non_field_errors[0] 
            : error.response.data.non_field_errors;
        }
        // Check for any error message in the response
        else if (typeof error.response.data === 'string') {
          errorMessage = error.response.data;
        }
        // Check for error in message field
        else if (error.response.data.message) {
          errorMessage = error.response.data.message;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      toast.error(errorMessage);
    }
  };

  return (
    <div className="post-card">
      <div className="post-header">
        <h3>{post.title}</h3>
        <span className="post-date">
          {new Date(post.created_at).toLocaleDateString()}
        </span>
      </div>
      <div className="post-content">{post.content}</div>
      <div className="post-footer">
        <span className="comment-count">
          {post.comment_count} {post.comment_count === 1 ? 'comment' : 'comments'}
        </span>
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
    </div>
  );
};

export default PostCard;
