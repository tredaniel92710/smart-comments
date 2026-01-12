import React, { useState } from 'react';
import './CommentForm.css';

interface CommentFormProps {
  onSubmit: (author: string, content: string, useMl: boolean, classifierType?: 'huggingface' | 'openai') => void;
}

const CommentForm: React.FC<CommentFormProps> = ({ onSubmit }) => {
  const [author, setAuthor] = useState('');
  const [content, setContent] = useState('');
  const [useMl, setUseMl] = useState(false);
  const [classifierType, setClassifierType] = useState<'huggingface' | 'openai'>('huggingface');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (author.trim() && content.trim()) {
      onSubmit(author.trim(), content.trim(), useMl, useMl ? classifierType : undefined);
      setAuthor('');
      setContent('');
      setUseMl(false);
      setClassifierType('huggingface');
    }
  };

  return (
    <form className="comment-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="author">Your Name</label>
        <input
          type="text"
          id="author"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          placeholder="Enter your name"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="content">Comment</label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your comment here..."
          rows={4}
          required
        />
      </div>
      <div className="form-group">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={useMl}
            onChange={(e) => setUseMl(e.target.checked)}
          />
          <span>Use ML classification (bonus feature)</span>
        </label>
      </div>
      {useMl && (
        <div className="form-group">
          <label htmlFor="classifier-type">Classifier Type</label>
          <select
            id="classifier-type"
            className="classifier-select"
            value={classifierType}
            onChange={(e) => setClassifierType(e.target.value as 'huggingface' | 'openai')}
          >
            <option value="huggingface">Hugging Face (Local)</option>
            <option value="openai">OpenAI API</option>
          </select>
        </div>
      )}
      <button type="submit" className="submit-btn">
        Submit Comment
      </button>
    </form>
  );
};

export default CommentForm;
