import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search, Sparkles } from "lucide-react";
import { api } from "../api/client";
import { SearchResult } from "../types";

const SAMPLE_QUERIES = [
  "Machine learning applications in healthcare.",
  "Research papers about edge computing and IoT.",
  "Natural language processing for sentiment analysis.",
  "Deep learning techniques for computer vision.",
];

export const SmartSearchPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialQ = searchParams.get("q") || "";
  const [query, setQuery] = useState(initialQ);
  const [mode, setMode] = useState<"hybrid" | "keyword">("hybrid");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState<any>(null);

  const runSearch = async (q: string, m = mode) => {
    if (!q.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await api.smartSearch(q.trim(), m, 15);
      setData(res);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Search request failed.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialQ) {
      setQuery(initialQ);
      runSearch(initialQ, mode);
    }
  }, [initialQ]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Smart Search</h1>
        <p className="text-sm text-slate-600 mt-1">
          Retrieve and rank academic papers using TF-IDF vectorization, cosine similarity, and keyword matching.
        </p>
      </div>

      <div className="card p-5 space-y-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            runSearch(query, mode);
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter a natural-language research query..."
              className="input-field pl-10"
            />
          </div>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value as "hybrid" | "keyword")}
            className="input-field sm:w-56"
          >
            <option value="hybrid">TF-IDF + Cosine Similarity</option>
            <option value="keyword">Keyword-Based Search</option>
          </select>
          <button type="submit" disabled={loading || !query.trim()} className="btn-primary">
            <Sparkles className="w-4 h-4" />
            {loading ? "Searching..." : "Search Papers"}
          </button>
        </form>

        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs text-slate-500">Try sample queries:</span>
          {SAMPLE_QUERIES.map((sq) => (
            <button
              key={sq}
              type="button"
              onClick={() => {
                setQuery(sq);
                runSearch(sq, mode);
              }}
              className="text-xs px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors"
            >
              {sq}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">{error}</div>
      )}

      {data && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-600 card px-4 py-3">
            <span>
              Method: <strong className="text-slate-900">{data.retrieval_method}</strong>
            </span>
            <span>Found {data.total_results} ranked matches</span>
          </div>

          {data.results.length === 0 ? (
            <div className="card p-8 text-center text-sm text-slate-500">
              No matching papers found for "{data.query}".
            </div>
          ) : (
            <div className="space-y-3">
              {data.results.map((r: SearchResult, idx: number) => (
                <div key={r.paper_id} className="card p-5 space-y-2.5">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-400">#{idx + 1}</span>
                      <span className="text-xs font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">
                        {r.paper_id}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-medium">
                        {r.research_domain}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="px-2.5 py-1 rounded-full bg-teal-50 text-teal-800 font-semibold">
                        Relevance: {(r.relevance_score * 100).toFixed(1)}%
                      </span>
                      <span className="text-slate-400">
                        TF-IDF: {r.tfidf_cosine_score.toFixed(3)}
                      </span>
                    </div>
                  </div>

                  <h3 className="text-base font-semibold text-slate-900">{r.title}</h3>
                  <p className="text-xs text-slate-500">
                    {r.authors} &middot; {r.publication_year} &middot; {r.methodology}
                  </p>
                  <p className="text-sm text-slate-700">{r.abstract_preview}</p>

                  {r.matching_keywords.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1.5 pt-1">
                      <span className="text-[11px] font-medium text-slate-500">Matching terms:</span>
                      {r.matching_keywords.map((kw) => (
                        <span key={kw} className="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                          {kw}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
