export interface Comment {
  id: number;
  post: number;
  author: string;
  content: string;
  created_at: string;
  flagged_for_review: boolean;
  flag_reason: string | null;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  comments: Comment[];
  comment_count: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
