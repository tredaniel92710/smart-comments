import React from 'react';
import { Comment } from '../types';
import './CommentItem.css';

interface CommentItemProps {
  comment: Comment;
}

const CommentItem: React.FC<CommentItemProps> = ({ comment }) => {
  return (
    <div
      className={`comment-item ${comment.flagged_for_review ? 'flagged' : ''}`}
    >
      <div className="comment-header">
        <span className="comment-author">{comment.author}</span>
        <span className="comment-date">
          {new Date(comment.created_at).toLocaleString()}
        </span>
        {comment.flagged_for_review && (
          <span className="flag-badge" title={comment.flag_reason || 'Flagged for review'}>
            ⚠️ Flagged
          </span>
        )}
      </div>
      <div className="comment-content">{comment.content}</div>
      {comment.flag_reason && (
        <div className="flag-reason">
          Reason: {comment.flag_reason}
        </div>
      )}
    </div>
  );
};

export default CommentItem;
