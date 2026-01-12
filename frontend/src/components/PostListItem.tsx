import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Post } from '../types';
import './PostListItem.css';

interface PostListItemProps {
  post: Post;
}

const PostListItem: React.FC<PostListItemProps> = ({ post }) => {
  const navigate = useNavigate();
  
  // Get preview of content (first 150 characters)
  const contentPreview = post.content && post.content.length > 150 
    ? post.content.substring(0, 150) + '...' 
    : post.content || '';

  const handleClick = () => {
    navigate(`/posts/${post.id}`);
  };

  const commentCount = post.comment_count || (post.comments ? post.comments.length : 0);

  return (
    <div className="post-list-item" onClick={handleClick}>
      <div className="post-list-item-header">
        <h3 className="post-list-item-title">{post.title}</h3>
        <span className="post-list-item-date">
          {new Date(post.created_at).toLocaleDateString()}
        </span>
      </div>
      {contentPreview && (
        <p className="post-list-item-preview">{contentPreview}</p>
      )}
      <div className="post-list-item-footer">
        <span className="post-list-item-comments">
          {commentCount} {commentCount === 1 ? 'comment' : 'comments'}
        </span>
      </div>
    </div>
  );
};

export default PostListItem;
