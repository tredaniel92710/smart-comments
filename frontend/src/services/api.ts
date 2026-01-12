import client from '../api/client';
import { Post, Comment, PaginatedResponse } from '../types';

export const postsApi = {
  getAll: async (page?: number, pageSize?: number): Promise<PaginatedResponse<Post> | Post[]> => {
    const params: any = {};
    if (page) params.page = page;
    if (pageSize) params.page_size = pageSize;
    
    const response = await client.get('/posts/', { params });
    // Return paginated response if it has pagination structure, otherwise return array
    if (response.data.results !== undefined) {
      return response.data as PaginatedResponse<Post>;
    }
    return Array.isArray(response.data) ? response.data : [];
  },

  getById: async (id: number): Promise<Post> => {
    const response = await client.get(`/posts/${id}/`);
    return response.data;
  },

  create: async (title: string, content: string): Promise<Post> => {
    const response = await client.post('/posts/', { title, content });
    return response.data;
  },
};

export const commentsApi = {
  getAll: async (postId?: number, flaggedOnly?: boolean): Promise<Comment[]> => {
    const params: any = {};
    if (postId) params.post = postId;
    if (flaggedOnly) params.flagged = 'true';
    
    const response = await client.get('/comments/', { params });
    // Handle paginated response from Django REST Framework
    return Array.isArray(response.data) ? response.data : response.data.results || [];
  },

  create: async (postId: number, author: string, content: string, useMl?: boolean, classifierType?: 'huggingface' | 'openai'): Promise<Comment> => {
    const params: any = {};
    if (useMl) params.use_ml = 'true';
    if (classifierType) params.classifier_type = classifierType;
    
    const response = await client.post('/comments/', {
      post: postId,
      author,
      content,
    }, { params });
    return response.data;
  },

  getFlagged: async (): Promise<Comment[]> => {
    const response = await client.get('/comments/flagged/');
    // Handle paginated response from Django REST Framework
    return Array.isArray(response.data) ? response.data : response.data.results || [];
  },

  getSettings: async (): Promise<{ comments_enabled: boolean }> => {
    const response = await client.get('/comments/settings/');
    return response.data;
  },
};
