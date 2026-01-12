import React, { useState, useEffect } from 'react';
import { Comment } from '../types';
import { commentsApi } from '../services/api';
import CommentItem from './CommentItem';
import './ModeratorView.css';

const ModeratorView: React.FC = () => {
  const [flaggedComments, setFlaggedComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFlaggedComments();
  }, []);

  const loadFlaggedComments = async () => {
    try {
      setLoading(true);
      const data = await commentsApi.getFlagged();
      setFlaggedComments(data);
      setError(null);
    } catch (err) {
      setError('Failed to load flagged comments');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading flagged comments...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="moderator-view">
      <div className="moderator-header">
        <h2>Moderator View</h2>
        <button onClick={loadFlaggedComments} className="refresh-btn">
          Refresh
        </button>
      </div>
      <div className="flagged-count">
        {flaggedComments.length} {flaggedComments.length === 1 ? 'comment' : 'comments'} flagged for review
      </div>
      {flaggedComments.length === 0 ? (
        <div className="empty-state">
          No flagged comments. All clear! ✅
        </div>
      ) : (
        <div className="flagged-comments-list">
          {flaggedComments.map((comment) => (
            <div key={comment.id} className="flagged-comment-wrapper">
              <CommentItem comment={comment} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModeratorView;
