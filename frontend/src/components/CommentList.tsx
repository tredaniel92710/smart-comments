import React from 'react';
import { Comment } from '../types';
import CommentItem from './CommentItem';
import './CommentList.css';

interface CommentListProps {
  comments: Comment[];
}

const CommentList: React.FC<CommentListProps> = ({ comments }) => {
  if (comments.length === 0) {
    return null;
  }

  return (
    <div className="comment-list">
      <h4>Comments</h4>
      {comments.map((comment) => (
        <CommentItem key={comment.id} comment={comment} />
      ))}
    </div>
  );
};

export default CommentList;
