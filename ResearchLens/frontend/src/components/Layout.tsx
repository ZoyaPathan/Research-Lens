import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  BarChart3,
  BookOpen,
  Compass,
  FileSearch,
  FlaskConical,
  GitBranch,
  Info,
  LayoutDashboard,
  Menu,
  MessageSquareText,
  Search,
  Sparkles,
  X,
} from "lucide-react";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/explorer", label: "Research Explorer", icon: BookOpen },
  { to: "/search", label: "Smart Search", icon: Search },
  { to: "/analyzer", label: "Paper Analyzer", icon: FileSearch, badge: "Unit I" },
  { to: "/nlp-lab", label: "NLP Lab", icon: FlaskConical, badge: "Unit II" },
  { to: "/semantic", label: "Semantic Analysis", icon: GitBranch, badge: "Unit III" },
  { to: "/discourse", label: "Discourse & Pragmatics", icon: MessageSquareText, badge: "Unit IV" },
  { to: "/summarizer", label: "AI Summarizer", icon: Sparkles, badge: "Unit V" },
  { to: "/insights", label: "Research Insights", icon: BarChart3 },
  { to: "/about", label: "About Project", icon: Info },
];

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [quickQuery, setQuickQuery] = useState("");
  const navigate = useNavigate();

  const handleQuickSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (quickQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(quickQuery.trim())}`);
      setQuickQuery("");
    }
  };

  return (
    <div className="min-h-screen flex bg-[#F8FAFC] text-[#0F172A]">
      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-slate-900/40 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-slate-200 flex flex-col transition-transform duration-200 lg:static lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="h-16 px-5 flex items-center justify-between border-b border-slate-200">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <div className="font-semibold text-sm tracking-tight text-slate-900">ResearchLens</div>
              <div className="text-[11px] text-slate-500">NLPLM Academic Suite</div>
            </div>
          </div>
          <button
            className="lg:hidden p-1 text-slate-500 hover:text-slate-800"
            onClick={() => setSidebarOpen(false)}
            aria-label="Close sidebar"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                onClick={() => setSidebarOpen(false)}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-slate-900 text-white"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  }`
                }
              >
                <span className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </span>
                {item.badge && (
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-200 text-xs text-slate-500">
          <div className="font-medium text-slate-700">NLPLM Units I–V</div>
          <div>Local FastAPI + SQLite + NLTK</div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Topbar */}
        <header className="h-16 bg-white border-b border-slate-200 px-4 lg:px-8 flex items-center justify-between gap-4 sticky top-0 z-20">
          <div className="flex items-center gap-3">
            <button
              className="lg:hidden p-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50"
              onClick={() => setSidebarOpen(true)}
              aria-label="Open menu"
            >
              <Menu className="w-4 h-4" />
            </button>
            <span className="hidden sm:inline text-sm font-medium text-slate-500">
              Academic Research Paper Analysis &amp; NLP Platform
            </span>
          </div>

          <form onSubmit={handleQuickSearch} className="flex-1 max-w-md flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={quickQuery}
                onChange={(e) => setQuickQuery(e.target.value)}
                placeholder="Quick semantic search (e.g., edge computing IoT)..."
                className="input-field pl-9 py-1.5"
              />
            </div>
            <button type="submit" className="btn-secondary py-1.5 px-3 text-xs">
              Search
            </button>
          </form>
        </header>

        <main className="flex-1 p-4 lg:p-8 max-w-7xl w-full mx-auto">{children}</main>
      </div>
    </div>
  );
};
