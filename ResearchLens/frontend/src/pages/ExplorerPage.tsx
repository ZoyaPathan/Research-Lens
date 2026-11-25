import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, ChevronLeft, ChevronRight, Eye, Search, X } from "lucide-react";
import { api } from "../api/client";
import { Paper } from "../types";

export const ExplorerPage: React.FC = () => {
  const [search, setSearch] = useState("");
  const [domain, setDomain] = useState("All");
  const [year, setYear] = useState("");
  const [sort, setSort] = useState("year_desc");
  const [page, setPage] = useState(1);
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);

  const { data: meta } = useQuery({
    queryKey: ["domains-meta"],
    queryFn: api.getDomains,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ["papers", search, domain, year, sort, page],
    queryFn: () =>
      api.getPapers({
        search: search || undefined,
        domain: domain === "All" ? undefined : domain,
        year: year ? Number(year) : undefined,
        sort,
        page,
        page_size: 9,
      }),
  });

  const papers: Paper[] = data?.items || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Research Explorer</h1>
        <p className="text-sm text-slate-600 mt-1">
          Browse, filter, and inspect synthetic academic research papers stored in SQLite.
        </p>
      </div>

      {/* Filters */}
      <div className="card p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search by title, author, keyword..."
            className="input-field pl-9"
          />
        </div>

        <select
          className="input-field"
          value={domain}
          onChange={(e) => {
            setDomain(e.target.value);
            setPage(1);
          }}
        >
          <option value="All">All Research Domains</option>
          {(meta?.domains || []).map((d: any) => (
            <option key={d.domain} value={d.domain}>
              {d.domain} ({d.count})
            </option>
          ))}
        </select>

        <select
          className="input-field"
          value={year}
          onChange={(e) => {
            setYear(e.target.value);
            setPage(1);
          }}
        >
          <option value="">All Publication Years</option>
          {(meta?.years || []).map((y: number) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>

        <select
          className="input-field"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
        >
          <option value="year_desc">Sort: Year (Newest First)</option>
          <option value="year_asc">Sort: Year (Oldest First)</option>
          <option value="title_asc">Sort: Title (A–Z)</option>
        </select>
      </div>

      {/* Results */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="card h-56 animate-pulse bg-slate-100" />
          ))}
        </div>
      ) : error ? (
        <div className="card p-6 text-sm text-red-700 bg-red-50 border-red-200">
          Error loading papers from backend.
        </div>
      ) : papers.length === 0 ? (
        <div className="card p-10 text-center text-sm text-slate-500">
          No research papers match the selected filters.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {papers.map((p) => (
            <div key={p.paper_id} className="card p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between gap-2 text-xs text-slate-500 mb-2">
                  <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">
                    {p.paper_id}
                  </span>
                  <span className="font-medium text-teal-700">{p.publication_year}</span>
                </div>
                <h3 className="text-sm font-semibold text-slate-900 leading-snug line-clamp-2">
                  {p.title}
                </h3>
                <p className="text-xs text-slate-500 mt-1">{p.authors}</p>
                <div className="mt-2 inline-block text-[11px] font-medium px-2 py-0.5 rounded bg-blue-50 text-blue-700">
                  {p.research_domain}
                </div>
                <p className="text-xs text-slate-600 mt-3 line-clamp-3">{p.abstract}</p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 truncate max-w-[160px]">
                  {p.methodology}
                </span>
                <button
                  onClick={() => setSelectedPaper(p)}
                  className="btn-secondary py-1 px-2.5 text-xs"
                >
                  <Eye className="w-3.5 h-3.5" /> Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {data && data.total_pages > 1 && (
        <div className="flex items-center justify-between card px-4 py-3 text-xs text-slate-600">
          <span>
            Showing page {data.page} of {data.total_pages} ({data.total} total papers)
          </span>
          <div className="flex items-center gap-2">
            <button
              className="btn-secondary py-1 px-2.5 text-xs"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              <ChevronLeft className="w-4 h-4" /> Prev
            </button>
            <button
              className="btn-secondary py-1 px-2.5 text-xs"
              disabled={page >= data.total_pages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Paper Detail Modal */}
      {selectedPaper && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-xl border border-slate-200 space-y-4">
            <div className="flex items-start justify-between gap-4">
              <div>
                <span className="text-xs font-mono text-slate-500">{selectedPaper.paper_id}</span>
                <h2 className="text-lg font-bold text-slate-900 mt-0.5">{selectedPaper.title}</h2>
              </div>
              <button
                onClick={() => setSelectedPaper(null)}
                className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-500"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex flex-wrap gap-2 text-xs">
              <span className="px-2.5 py-1 rounded bg-blue-50 text-blue-700 font-medium">
                {selectedPaper.research_domain}
              </span>
              <span className="px-2.5 py-1 rounded bg-teal-50 text-teal-700 font-medium">
                Year: {selectedPaper.publication_year}
              </span>
              <span className="px-2.5 py-1 rounded bg-slate-100 text-slate-700 font-medium">
                Methodology: {selectedPaper.methodology}
              </span>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-500">Authors</h4>
              <p className="text-sm text-slate-800 mt-1">{selectedPaper.authors}</p>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-500">Abstract</h4>
              <p className="text-sm text-slate-700 leading-relaxed mt-1">{selectedPaper.abstract}</p>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-500 mb-1.5">Keywords</h4>
              <div className="flex flex-wrap gap-1.5">
                {selectedPaper.keywords_list.map((kw) => (
                  <span key={kw} className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-xs">
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
