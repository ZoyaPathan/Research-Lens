export interface Paper {
  paper_id: string;
  title: string;
  abstract: string;
  authors: string;
  research_domain: string;
  keywords: string;
  keywords_list: string[];
  methodology: string;
  publication_year: number;
}

export interface PaginatedPapers {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  items: Paper[];
}

export interface SearchResult {
  paper_id: string;
  title: string;
  abstract_preview: string;
  authors: string;
  research_domain: string;
  publication_year: number;
  methodology: string;
  relevance_score: number;
  tfidf_cosine_score: number;
  keyword_match_score: number;
  matching_keywords: string[];
}
