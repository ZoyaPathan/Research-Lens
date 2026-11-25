import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const api = {
  getHealth: () => apiClient.get("/health").then((r) => r.data),

  getPapers: (params: {
    search?: string;
    domain?: string;
    year?: number | string;
    sort?: string;
    page?: number;
    page_size?: number;
  }) => apiClient.get("/papers", { params }).then((r) => r.data),

  getPaper: (paperId: string) => apiClient.get(`/papers/${paperId}`).then((r) => r.data),

  getDomains: () => apiClient.get("/domains").then((r) => r.data),

  smartSearch: (q: string, mode = "hybrid", top_k = 15) =>
    apiClient.get("/search", { params: { q, mode, top_k } }).then((r) => r.data),

  analyzeUnit1: (text: string, paper_id?: string) =>
    apiClient.post("/analyze", { text, paper_id }).then((r) => r.data),

  posTag: (text: string, paper_id?: string) =>
    apiClient.post("/nlp/pos-tag", { text, paper_id }).then((r) => r.data),

  tfidf: (payload: { text?: string; paper_id?: string; top_k?: number }) =>
    apiClient.post("/nlp/tfidf", payload).then((r) => r.data),

  ngrams: (payload: { text?: string; context?: string; n?: number }) =>
    apiClient.post("/nlp/ngrams", payload).then((r) => r.data),

  extractInfo: (text: string, paper_id?: string) =>
    apiClient.post("/nlp/extract", { text, paper_id }).then((r) => r.data),

  wordnet: (payload: { word: string; sentence?: string; compare_word?: string }) =>
    apiClient.post("/nlp/wordnet", payload).then((r) => r.data),

  semanticSimilarity: (sentence1: string, sentence2: string, method = "auto") =>
    apiClient.post("/semantic/similarity", { sentence1, sentence2, method }).then((r) => r.data),

  semanticAnalyze: (text: string, target_word?: string, paper_id?: string) =>
    apiClient.post("/semantic/analyze", { text, target_word, paper_id }).then((r) => r.data),

  discourseAnalyze: (text: string, paper_id?: string) =>
    apiClient.post("/discourse/analyze", { text, paper_id }).then((r) => r.data),

  discourseConversation: (conversation: string) =>
    apiClient.post("/discourse/conversation", { conversation }).then((r) => r.data),

  summarizeStatus: () => apiClient.get("/summarize/status").then((r) => r.data),

  summarize: (payload: {
    text: string;
    paper_id?: string;
    length?: string;
    instruction?: string;
    use_hf?: boolean;
  }) => apiClient.post("/summarize", payload).then((r) => r.data),

  evaluateSummary: (generated_summary: string, reference_summary: string) =>
    apiClient
      .post("/summarize/evaluate", { generated_summary, reference_summary })
      .then((r) => r.data),

  getInsightsOverview: () => apiClient.get("/insights/overview").then((r) => r.data),
  getInsightsDomains: () => apiClient.get("/insights/domains").then((r) => r.data),
  getInsightsKeywords: () => apiClient.get("/insights/keywords").then((r) => r.data),
};
