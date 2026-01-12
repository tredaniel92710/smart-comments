import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Post, PaginatedResponse } from '../types';
import { postsApi } from '../services/api';
import PostListItem from './PostListItem';
import Pagination from './Pagination';
import './PostList.css';

const POSTS_PER_PAGE = 10;

const PostList: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    const page = parseInt(searchParams.get('page') || '1', 10);
    setCurrentPage(page);
    loadPosts(page);
  }, [searchParams]);

  const loadPosts = async (page: number) => {
    try {
      setLoading(true);
      const data = await postsApi.getAll(page, POSTS_PER_PAGE);
      
      if (Array.isArray(data)) {
        // Non-paginated response
        setPosts(data);
        setTotalPages(1);
        setTotalCount(data.length);
      } else {
        // Paginated response
        const paginatedData = data as PaginatedResponse<Post>;
        setPosts(paginatedData.results);
        setTotalCount(paginatedData.count);
        // Calculate total pages
        const pages = Math.ceil(paginatedData.count / POSTS_PER_PAGE);
        setTotalPages(pages || 1);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load posts');
      console.error(err);
      setPosts([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page: number) => {
    setSearchParams({ page: page.toString() });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return <div className="loading">Loading posts...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="post-list">
      <div className="post-list-header">
        <h2>Posts</h2>
        {totalCount > 0 && (
          <span className="post-list-count">
            {totalCount} {totalCount === 1 ? 'post' : 'posts'}
          </span>
        )}
      </div>
      
      {posts.length === 0 ? (
        <div className="empty-state">No posts yet. Create one to get started!</div>
      ) : (
        <>
          <div className="post-list-items">
            {posts.map((post) => (
              <PostListItem key={post.id} post={post} />
            ))}
          </div>
          
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
        </>
      )}
    </div>
  );
};

export default PostList;
