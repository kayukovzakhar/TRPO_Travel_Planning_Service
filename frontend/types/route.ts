export type RouteCategory = 'nature' | 'culture' | 'adventure' | 'relax';

export interface Route {
  id: string;
  title: string;
  description: string;
  category: RouteCategory;
  details?: string;
  checklist?: {
    title: string;
    description: string;
    photo: string;
  }[];
} 