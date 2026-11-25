import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { BookOpen, FileCheck2, FolderKanban, Hash, ArrowRight } from "lucide-react";
import { api } from "../api/client";

export const DashboardPage: React.FC = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["insights-overview"],
    queryFn: api.getInsightsOverview,
  });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="h-28 card animate-pulse bg-slate-100" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-28 card animate-pulse bg-slate-100" />
          ))}
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="card p-6 border-red-200 bg-red-50 text-red-800 text-sm">
        Failed to load dashboard analytics from the backend. Ensure FastAPI is running on port 8000.
      </div>
    );
  }

  const stats = [
    {
      label: "Total Research Papers",
      value: data.total_papers,
      icon: BookOpen,
      accent: "text-blue-700 bg-blue-50",
    },
    {
      label: "Research Domains",
      value: data.total_domains,
      icon: FolderKanban,
      accent: "text-teal-700 bg-teal-50",
    },
    {
      label: "Total Analyses Run",
      value: data.total_analyzed_papers,
      icon: FileCheck2,
      accent: "text-slate-700 bg-slate-100",
    },
    {
      label: "Unique Extracted Keywords",
      value: data.total_unique_keywords,
      icon: Hash,
      accent: "text-indigo-700 bg-indigo-50",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Intro Banner */}
      <section className="card p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-teal-700">
              Natural Language Processing &amp; Language Models (NLPLM)
            </span>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">
              Welcome to ResearchLens
            </h1>
            <p className="text-sm text-slate-600 mt-1.5 max-w-3xl">
              ResearchLens is an academic research paper analysis, semantic search, and summarization platform.
              Explore {data.total_papers} synthetic academic papers and demonstrate NLP techniques from Units I–V
              using live FastAPI, NLTK, Scikit-learn, and Hugging Face Transformers pipelines.
            </p>
          </div>
          <div className="flex flex-wrap gap-2 shrink-0">
            <Link to="/search" className="btn-primary">
              Smart Search <ArrowRight className="w-4 h-4" />
            </Link>
            <Link to="/analyzer" className="btn-secondary">
              Open Paper Analyzer
            </Link>
          </div>
        </div>
      </section>

      {/* KPI Cards */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s) => {
          const Icon = s.icon;
          return (
            <div key={s.label} className="card p-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-slate-500">{s.label}</p>
                <p className="text-2xl font-bold text-slate-900 mt-1">{s.value}</p>
              </div>
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${s.accent}`}>
                <Icon className="w-5 h-5" />
              </div>
            </div>
          );
        })}
      </section>

      {/* Charts */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-5">
          <h2 className="text-sm font-semibold text-slate-900 mb-4">
            Research Domain Distribution
          </h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.popular_domains} layout="vertical" margin={{ left: 10, right: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis type="number" tick={{ fontSize: 12, fill: "#475569" }} />
                <YAxis
                  dataKey="domain"
                  type="category"
                  width={150}
                  tick={{ fontSize: 11, fill: "#334155" }}
                />
                <Tooltip />
                <Bar dataKey="count" fill="#1D4ED8" radius={[0, 4, 4, 0]} name="Papers" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card p-5">
          <h2 className="text-sm font-semibold text-slate-900 mb-4">
            Publication Year Distribution (2020–2026)
          </h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.year_distribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="year" tick={{ fontSize: 12, fill: "#475569" }} />
                <YAxis tick={{ fontSize: 12, fill: "#475569" }} />
                <Tooltip />
                <Bar dataKey="count" fill="#0F766E" radius={[4, 4, 0, 0]} name="Papers" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Recent Papers & Top Keywords */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card p-5 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-slate-900">Recently Added Papers</h2>
            <Link to="/explorer" className="text-xs font-medium text-blue-700 hover:underline">
              View all papers
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {data.recent_papers.map((p: any) => (
              <div key={p.paper_id} className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <div className="text-sm font-medium text-slate-900">{p.title}</div>
                  <div className="text-xs text-slate-500 mt-0.5">
                    {p.authors} &middot; {p.research_domain}
                  </div>
                </div>
                <span className="text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-medium shrink-0 self-start sm:self-center">
                  {p.publication_year}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="card p-5">
          <h2 className="text-sm font-semibold text-slate-900 mb-4">
            Frequently Occurring Keywords
          </h2>
          <div className="flex flex-wrap gap-2">
            {data.top_keywords.map((kw: any) => (
              <Link
                key={kw.keyword}
                to={`/search?q=${encodeURIComponent(kw.keyword)}`}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-xs text-slate-700 transition-colors"
              >
                <span>{kw.keyword}</span>
                <span className="text-[10px] font-semibold text-slate-500">{kw.count}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
