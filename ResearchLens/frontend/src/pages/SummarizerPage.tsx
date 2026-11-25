import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Sparkles } from "lucide-react";
import { api } from "../api/client";
import { PaperSelector } from "../components/PaperSelector";

const DEFAULT_ABSTRACT =
  "Research in natural language processing increasingly demands robust solutions for abstractive summarization of biomedical literature. However, existing approaches often struggle with scalability, domain shift, and factual hallucinations when deployed on long clinical documents. In this paper, we propose a Retrieval-Augmented Transformer architecture specifically designed to ground generated summaries in source evidence. We evaluate our methodology across annotated clinical narrative corpora and compare it against established baseline models. Experimental results demonstrate that the proposed framework improves ROUGE-L by 5.2 points, while maintaining practical computational overhead for real-world deployment.";

const LLM_CONCEPTS = [
  { name: "RNNs", desc: "Recurrent Neural Networks process sequences step-by-step via hidden states, struggling with long-range dependencies." },
  { name: "Transformers", desc: "Parallel sequence architecture replacing recurrence with self-attention to model global token relationships." },
  { name: "Self-Attention", desc: "Computes weighted interactions between every pair of tokens (Query, Key, Value) in a sequence." },
  { name: "Multi-Head Attention", desc: "Runs multiple attention projections in parallel to capture syntactic, semantic, and positional patterns." },
  { name: "Positional Encoding", desc: "Injects token order information into embeddings since self-attention is permutation-invariant." },
  { name: "GPT (Autoregressive)", desc: "Decoder-only causal language model predicting the next token left-to-right." },
  { name: "BERT (Masked LM)", desc: "Bidirectional encoder trained to reconstruct masked tokens using both left and right context." },
  { name: "Fine-Tuning", desc: "Adapting a pretrained language model's weights to a downstream task on labeled data." },
  { name: "LoRA & Adapters", desc: "Parameter-efficient fine-tuning (PEFT) injecting low-rank matrices or small bottleneck layers while freezing base weights." },
  { name: "Prompt Tuning & In-Context Learning", desc: "Guiding frozen LLMs via learnable soft prompts or few-shot examples inside the input context." },
  { name: "Hallucination & Bias", desc: "Models may generate fluent but factually ungrounded claims or reflect societal biases from training corpora." },
];

export const SummarizerPage: React.FC = () => {
  const [text, setText] = useState(DEFAULT_ABSTRACT);
  const [paperId, setPaperId] = useState<string | undefined>(undefined);
  const [length, setLength] = useState<"short" | "detailed">("short");
  const [instruction, setInstruction] = useState("researcher");
  const [useHf, setUseHf] = useState(false);

  const [sumRes, setSumRes] = useState<any>(null);
  const [refSummary, setRefSummary] = useState(
    "A retrieval-augmented transformer architecture grounds clinical summaries in source evidence and improves ROUGE-L by 5.2 points."
  );
  const [rougeRes, setRougeRes] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { data: statusData } = useQuery({
    queryKey: ["summarizer-status"],
    queryFn: api.summarizeStatus,
  });

  const handleSummarize = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.summarize({ text, paper_id: paperId, length, instruction, use_hf: useHf });
      setSumRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Summarization failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    if (!sumRes?.summary || !refSummary.trim()) return;
    setError("");
    try {
      const data = await api.evaluateSummary(sumRes.summary, refSummary);
      setRougeRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "ROUGE evaluation failed.");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-teal-700">Unit V</span>
          <h1 className="text-xl font-bold text-slate-900">AI Summarizer &amp; Language Models</h1>
          <p className="text-sm text-slate-600 mt-1">
            Hugging Face Transformers pipeline (lazy-loaded with extractive fallback), Prompt Engineering, ROUGE evaluation, and LLM concepts.
          </p>
        </div>
        {statusData && (
          <div className="text-xs px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 shrink-0">
            HF Model: <strong>{statusData.status}</strong> ({statusData.model_name})
          </div>
        )}
      </div>

      {error && <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">{error}</div>}

      <div className="card p-5 space-y-4">
        <PaperSelector
          selectedId={paperId}
          onSelect={(p) => {
            setPaperId(p.paper_id);
            setText(p.abstract);
          }}
        />
        <textarea
          rows={4}
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            setPaperId(undefined);
          }}
          className="input-field"
        />

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">Summary Length</label>
            <select value={length} onChange={(e) => setLength(e.target.value as any)} className="input-field">
              <option value="short">Short Summary</option>
              <option value="detailed">Detailed Summary</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">Prompt Instruction Template</label>
            <select value={instruction} onChange={(e) => setInstruction(e.target.value)} className="input-field">
              <option value="beginner">1. Summarize for a beginner</option>
              <option value="researcher">2. Summarize for a researcher</option>
              <option value="bullets">3. Summarize in five bullet points</option>
              <option value="methodology">4. Explain the research methodology</option>
              <option value="findings">5. Extract the main findings</option>
            </select>
          </div>

          <div className="flex items-center justify-between gap-3">
            <label className="flex items-center gap-2 text-xs text-slate-600 cursor-pointer">
              <input
                type="checkbox"
                checked={useHf}
                onChange={(e) => setUseHf(e.target.checked)}
                className="rounded border-slate-300"
              />
              Try HF Pipeline
            </label>
            <button onClick={handleSummarize} disabled={loading} className="btn-primary">
              <Sparkles className="w-4 h-4" />
              {loading ? "Summarizing..." : "Generate Summary"}
            </button>
          </div>
        </div>
      </div>

      {sumRes && (
        <div className="card p-5 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h2 className="text-sm font-semibold text-slate-900">Generated Summary</h2>
            <span className="text-xs px-2.5 py-1 rounded bg-blue-50 text-blue-700 font-medium">
              {sumRes.method_used}
            </span>
          </div>
          <div className="text-xs p-3 rounded bg-slate-50 border border-slate-200 text-slate-600">
            <strong>Prompt Template:</strong> {sumRes.prompt_template_used}
            <div className="text-[11px] text-slate-400 mt-0.5">{sumRes.prompt_note}</div>
          </div>
          <div className="p-4 rounded-lg bg-white border border-slate-200 text-sm text-slate-800 whitespace-pre-line leading-relaxed">
            {sumRes.summary}
          </div>

          {/* ROUGE Evaluation */}
          <div className="pt-3 border-t border-slate-200 space-y-3">
            <h3 className="text-xs font-semibold uppercase text-slate-500">
              ROUGE Summarization Evaluation (Compare vs Reference Summary)
            </h3>
            <textarea
              rows={2}
              value={refSummary}
              onChange={(e) => setRefSummary(e.target.value)}
              className="input-field text-xs"
              placeholder="Enter a reference summary to compute ROUGE-1, ROUGE-2, and ROUGE-L..."
            />
            <button onClick={handleEvaluate} className="btn-secondary text-xs">
              Compute ROUGE Scores
            </button>

            {rougeRes && (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                {[
                  { label: "ROUGE-1 (Unigram)", data: rougeRes.rouge1 },
                  { label: "ROUGE-2 (Bigram)", data: rougeRes.rouge2 },
                  { label: "ROUGE-L (LCS)", data: rougeRes.rougeL },
                ].map((m) => (
                  <div key={m.label} className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <div className="font-semibold text-slate-800">{m.label}</div>
                    <div className="mt-1 font-mono text-teal-800">F1: {m.data.fmeasure}</div>
                    <div className="text-slate-500">
                      P: {m.data.precision} &middot; R: {m.data.recall}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* LLM Concepts */}
      <div className="card p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">
          Unit V Concepts: Sequence Models, Transformers, Fine-Tuning &amp; Prompting
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {LLM_CONCEPTS.map((c) => (
            <div key={c.name} className="p-3.5 rounded-lg bg-slate-50 border border-slate-200">
              <div className="text-xs font-semibold text-slate-900">{c.name}</div>
              <p className="text-xs text-slate-600 mt-1">{c.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
