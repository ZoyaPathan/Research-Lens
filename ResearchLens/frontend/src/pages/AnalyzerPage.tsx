import React, { useState } from "react";
import { FileSearch } from "lucide-react";
import { api } from "../api/client";
import { PaperSelector } from "../components/PaperSelector";

const DEFAULT_TEXT =
  "In 2025, federated learning models improved clinical diagnostics by 14.5% across multi-center hospital registries. However, existing approaches struggle with non-IID data distribution and privacy leakage. Contact research-team@university.edu for benchmark datasets.";

export const AnalyzerPage: React.FC = () => {
  const [text, setText] = useState(DEFAULT_TEXT);
  const [paperId, setPaperId] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [res, setRes] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.analyzeUnit1(text, paperId);
      setRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <span className="text-xs font-semibold uppercase tracking-wider text-teal-700">Unit I</span>
        <h1 className="text-xl font-bold text-slate-900">Paper Analyzer — Introduction &amp; Word Analysis</h1>
        <p className="text-sm text-slate-600 mt-1">
          Demonstrates Tokenization, Normalization, Stop-word Removal, Stemming, Lemmatization, Bag of Words, N-grams, Regex, Morphology, and FSA/FST.
        </p>
      </div>

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
          placeholder="Paste a research abstract here..."
        />
        <div className="flex justify-end">
          <button onClick={handleAnalyze} disabled={loading || !text.trim()} className="btn-primary">
            <FileSearch className="w-4 h-4" />
            {loading ? "Analyzing..." : "Analyze Text"}
          </button>
        </div>
      </div>

      {error && <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">{error}</div>}

      {res && (
        <div className="space-y-6">
          {/* A. Tokenization & B. Normalization */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card p-5 space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-900">A. Tokenization</h2>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700">
                  {res.tokenization.total_token_count} tokens
                </span>
              </div>
              <p className="text-xs text-slate-500">{res.tokenization.explanation}</p>
              <div className="flex flex-wrap gap-1.5 max-h-40 overflow-y-auto p-2 bg-slate-50 rounded-lg border border-slate-200">
                {res.tokenization.tokens.map((t: string, i: number) => (
                  <span key={i} className="text-xs px-2 py-0.5 bg-white border border-slate-200 rounded font-mono">
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">B. Text Normalization</h2>
              <p className="text-xs text-slate-500">{res.normalization.explanation}</p>
              <div className="text-xs bg-slate-50 p-3 rounded-lg border border-slate-200 font-mono text-slate-800 max-h-40 overflow-y-auto">
                {res.normalization.normalized_text}
              </div>
            </div>
          </div>

          {/* C. Stop-word Removal */}
          <div className="card p-5 space-y-3">
            <h2 className="text-sm font-semibold text-slate-900">C. Stop-word Removal</h2>
            <p className="text-xs text-slate-500">{res.stopword_removal.explanation}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-xs font-medium text-slate-600 mb-1.5">
                  Removed Stop Words ({res.stopword_removal.removed_stopwords.length})
                </div>
                <div className="flex flex-wrap gap-1.5 p-2.5 bg-red-50/50 border border-red-100 rounded-lg">
                  {res.stopword_removal.removed_stopwords.map((w: string, i: number) => (
                    <span key={i} className="text-xs px-2 py-0.5 rounded bg-white border border-red-200 text-red-700">
                      {w}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <div className="text-xs font-medium text-slate-600 mb-1.5">
                  Remaining Content Tokens ({res.stopword_removal.remaining_tokens.length})
                </div>
                <div className="flex flex-wrap gap-1.5 p-2.5 bg-teal-50/50 border border-teal-100 rounded-lg">
                  {res.stopword_removal.remaining_tokens.map((w: string, i: number) => (
                    <span key={i} className="text-xs px-2 py-0.5 rounded bg-white border border-teal-200 text-teal-800">
                      {w}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* D. Stemming & E. Lemmatization */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">D. Stemming ({res.stemming.method})</h2>
              <p className="text-xs text-slate-500">{res.stemming.explanation}</p>
              <div className="max-h-60 overflow-y-auto border border-slate-200 rounded-lg">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-600 sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Original Word</th>
                      <th className="px-3 py-2">Stemmed Word</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {res.stemming.rows.map((r: any, i: number) => (
                      <tr key={i}>
                        <td className="px-3 py-1.5 font-mono">{r.original}</td>
                        <td className="px-3 py-1.5 font-mono text-blue-700">{r.stemmed}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">E. Lemmatization ({res.lemmatization.method})</h2>
              <p className="text-xs text-slate-500">{res.lemmatization.note}</p>
              <div className="max-h-60 overflow-y-auto border border-slate-200 rounded-lg">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-600 sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Original Word</th>
                      <th className="px-3 py-2">Lemmatized Word</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {res.lemmatization.rows.map((r: any, i: number) => (
                      <tr key={i}>
                        <td className="px-3 py-1.5 font-mono">{r.original}</td>
                        <td className="px-3 py-1.5 font-mono text-teal-700">{r.lemmatized}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* F. Bag of Words & G. N-grams */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">F. Bag of Words (CountVectorizer)</h2>
              <p className="text-xs text-slate-500">{res.bag_of_words.explanation}</p>
              <div className="flex flex-wrap gap-1.5">
                {res.bag_of_words.word_frequencies.map((wf: any) => (
                  <span key={wf.term} className="text-xs px-2.5 py-1 rounded bg-slate-100 text-slate-800">
                    {wf.term}: <strong>{wf.count}</strong>
                  </span>
                ))}
              </div>
            </div>

            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">G. N-gram Analysis</h2>
              <p className="text-xs text-slate-500">{res.ngrams.explanation}</p>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <div>
                  <div className="font-semibold text-slate-700 mb-1">Unigrams</div>
                  {res.ngrams.unigrams.slice(0, 6).map((g: any, i: number) => (
                    <div key={i} className="py-0.5 text-slate-600">{g.ngram} ({g.count})</div>
                  ))}
                </div>
                <div>
                  <div className="font-semibold text-slate-700 mb-1">Bigrams</div>
                  {res.ngrams.bigrams.slice(0, 6).map((g: any, i: number) => (
                    <div key={i} className="py-0.5 text-slate-600">{g.ngram} ({g.count})</div>
                  ))}
                </div>
                <div>
                  <div className="font-semibold text-slate-700 mb-1">Trigrams</div>
                  {res.ngrams.trigrams.slice(0, 6).map((g: any, i: number) => (
                    <div key={i} className="py-0.5 text-slate-600">{g.ngram} ({g.count})</div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* H. Regex */}
          <div className="card p-5 space-y-3">
            <h2 className="text-sm font-semibold text-slate-900">H. Regular Expression Pattern Extraction</h2>
            <p className="text-xs text-slate-500">{res.regex.explanation}</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div className="font-semibold text-slate-700 mb-1">Emails</div>
                {res.regex.emails.length ? res.regex.emails.join(", ") : "No email matches found."}
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div className="font-semibold text-slate-700 mb-1">Years</div>
                {res.regex.years.length ? res.regex.years.join(", ") : "No year matches found."}
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div className="font-semibold text-slate-700 mb-1">Numbers / Metrics</div>
                {res.regex.numbers.length ? res.regex.numbers.join(", ") : "No numeric matches found."}
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div className="font-semibold text-slate-700 mb-1">Technical Patterns</div>
                {res.regex.technical_patterns.length ? res.regex.technical_patterns.join(", ") : "No acronyms/hyphenated terms."}
              </div>
            </div>
          </div>

          {/* I. Morphology & J. Finite Automata */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">I. Morphological Analysis</h2>
              <p className="text-xs text-slate-600">{res.morphology.explanation}</p>
              <div className="max-h-56 overflow-y-auto border border-slate-200 rounded-lg">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-600 sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Word</th>
                      <th className="px-3 py-2">Type</th>
                      <th className="px-3 py-2">Affix</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {res.morphology.tokens_analyzed.map((m: any, i: number) => (
                      <tr key={i}>
                        <td className="px-3 py-1.5 font-mono">{m.word}</td>
                        <td className="px-3 py-1.5">{m.morphology_type}</td>
                        <td className="px-3 py-1.5 font-mono text-teal-700">{m.detected_affix}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">J. Finite Automata (FSA) &amp; Transducers (FST)</h2>
              <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded px-2.5 py-1.5">
                {res.finite_automata.note}
              </p>
              <div className="text-xs space-y-2">
                <div className="font-semibold text-slate-700">FSA (-ing suffix recognizer):</div>
                <div className="flex flex-wrap gap-2">
                  {res.finite_automata.fsa_ing_recognizer.map((f: any, i: number) => (
                    <span
                      key={i}
                      className={`px-2.5 py-1 rounded border ${
                        f.accepted ? "bg-teal-50 border-teal-200 text-teal-800" : "bg-slate-50 border-slate-200 text-slate-600"
                      }`}
                    >
                      {f.word} &rarr; {f.accepted ? "ACCEPT" : "REJECT"} ({f.final_state})
                    </span>
                  ))}
                </div>
                <div className="font-semibold text-slate-700 pt-2">FST (inflected &rarr; base form):</div>
                <div className="space-y-1">
                  {res.finite_automata.fst_base_form.map((t: any, i: number) => (
                    <div key={i} className="text-slate-700 font-mono">
                      {t.input} &rarr; <strong className="text-blue-700">{t.base_form}</strong>{" "}
                      <span className="text-slate-400 font-sans">({t.rule})</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
