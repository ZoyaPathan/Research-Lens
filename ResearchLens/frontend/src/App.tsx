import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Layout } from "./components/Layout";
import { DashboardPage } from "./pages/DashboardPage";
import { ExplorerPage } from "./pages/ExplorerPage";
import { SmartSearchPage } from "./pages/SmartSearchPage";
import { AnalyzerPage } from "./pages/AnalyzerPage";
import { NlpLabPage } from "./pages/NlpLabPage";
import { SemanticPage } from "./pages/SemanticPage";
import { DiscoursePage } from "./pages/DiscoursePage";
import { SummarizerPage } from "./pages/SummarizerPage";
import { InsightsPage } from "./pages/InsightsPage";
import { AboutPage } from "./pages/AboutPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/explorer" element={<ExplorerPage />} />
            <Route path="/search" element={<SmartSearchPage />} />
            <Route path="/analyzer" element={<AnalyzerPage />} />
            <Route path="/nlp-lab" element={<NlpLabPage />} />
            <Route path="/semantic" element={<SemanticPage />} />
            <Route path="/discourse" element={<DiscoursePage />} />
            <Route path="/summarizer" element={<SummarizerPage />} />
            <Route path="/insights" element={<InsightsPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
