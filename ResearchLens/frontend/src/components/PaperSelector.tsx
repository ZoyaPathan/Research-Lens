import React from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import { Paper } from "../types";

interface PaperSelectorProps {
  onSelect: (paper: Paper) => void;
  selectedId?: string;
}

export const PaperSelector: React.FC<PaperSelectorProps> = ({ onSelect, selectedId }) => {
  const { data } = useQuery({
    queryKey: ["papers-selector"],
    queryFn: () => api.getPapers({ page: 1, page_size: 40 }),
  });

  const papers: Paper[] = data?.items || [];

  return (
    <div className="flex flex-col sm:flex-row sm:items-center gap-2">
      <label className="text-xs font-medium text-slate-600 shrink-0">
        Load Existing Paper:
      </label>
      <select
        className="input-field text-xs py-1.5"
        value={selectedId || ""}
        onChange={(e) => {
          const found = papers.find((p) => p.paper_id === e.target.value);
          if (found) onSelect(found);
        }}
      >
        <option value="">-- Select a paper from SQLite dataset --</option>
        {papers.map((p) => (
          <option key={p.paper_id} value={p.paper_id}>
            [{p.paper_id}] {p.title} ({p.publication_year})
          </option>
        ))}
      </select>
    </div>
  );
};
