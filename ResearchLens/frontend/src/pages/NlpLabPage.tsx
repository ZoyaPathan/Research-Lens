import React, { useState } from "react";
import { FlaskConical } from "lucide-react";
import { api } from "../api/client";
import { PaperSelector } from "../components/PaperSelector";

const DEFAULT_TEXT =
  "We propose a Federated Learning framework using Transformer encoders and Differential Privacy for clinical diagnostics on Kubernetes clusters.";

export const NlpLabPage: React.FC = () => {
  const [text, setText] = useState(DEFAULT_TEXT);
  const [paperId, setPaperId] = useState<string | undefined>(undefined);
  const [ngramContext, setNgramContext] = useState("deep learning");
  const [ngramOrder, setNgramOrder] = useState(2);

  const [wnWord, setWnWord] = useState("bank");
  const [wnSentence, setWnSentence] = useState("The researcher deposited the grant funds at the commercial bank.");
  const [wnCompare, setWnCompare] = useState("institution");

  const [loading, setLoading] = useState(false);
  const [posRes, setPosRes] = useState<any>(null);
  const [tfidfRes, setTfidfRes] = useState<any>(null);
  const [ngramRes, setNgramRes] = useState<any>(null);
  const [extractRes, setExtractRes] = useState<any>(null);
  const [wnRes, setWnRes] = useState<any>(null);
  const [error, setError] = useState("");

  const runAllTextLabs = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    try {
      const [pos, tfidf, ext, ng] = await Promise.all([
        api.posTag(text, paperId),
        api.tfidf({ text, paper_id: paperId, top_k: 10 }),
        api.extractInfo(text, paperId),
        api.ngrams({ text, context: ngramContext, n: ngramOrder }),
      ]);
      setPosRes(pos);
      setTfidfRes(tfidf);
      setExtractRes(ext);
      setNgramRes(ng);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "NLP Lab request failed.");
    } finally {
      setLoading(false);
    }
  };

  const runWordNet = async () => {
    if (!wnWord.trim()) return;
    setError("");
    try {
      const data = await api.wordnet({
        word: wnWord.trim(),
        sentence: wnSentence.trim() || undefined,
        compare_word: wnCompare.trim() || undefined,
      });
      setWnRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "WordNet analysis failed.");
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <span className="text-xs font-semibold uppercase tracking-wider text-teal-700">Unit II</span>
        <h1 className="text-xl font-bold text-slate-900">NLP Lab — Syntax, Lexical Semantics &amp; Language Models</h1>
        <p className="text-sm text-slate-600 mt-1">
          Interactive experiments for POS Tagging, TF-IDF, N-gram Language Models, Information Extraction, WordNet Semantics, WSD (Lesk), and Word Similarity.
        </p>
      </div>

      {/* Input Panel */}
      <div className="card p-5 space-y-4">
        <PaperSelector
          selectedId={paperId}
          onSelect={(p) => {
            setPaperId(p.paper_id);
            setText(p.abstract);
          }}
        />
        <textarea
          rows={3}
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            setPaperId(undefined);
          }}
          className="input-field"
          placeholder="Enter academic text for POS tagging, TF-IDF, and Information Extraction..."
        />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">N-gram Context (1–2 words)</label>
            <input
              type="text"
              value={ngramContext}
              onChange={(e) => setNgramContext(e.target.value)}
              className="input-field"
              placeholder="e.g., deep learning"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">N-gram Model Order</label>
            <select
              value={ngramOrder}
              onChange={(e) => setNgramOrder(Number(e.target.value))}
              className="input-field"
            >
              <option value={2}>Bigram (n = 2)</option>
              <option value={3}>Trigram (n = 3)</option>
              <option value={1}>Unigram (n = 1)</option>
            </select>
          </div>
          <button onClick={runAllTextLabs} disabled={loading} className="btn-primary w-full">
            <FlaskConical className="w-4 h-4" />
            {loading ? "Running Lab..." : "Run POS, TF-IDF, N-gram & IE"}
          </button>
        </div>
      </div>

      {error && <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">{error}</div>}

      {/* A. POS Tagging & B. TF-IDF */}
      {(posRes || tfidfRes) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {posRes && (
            <div className="card p-5 space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-900">A. POS Tagging</h2>
                <span className="text-[11px] text-slate-500">{posRes.engine_used}</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {posRes.category_distribution.map((c: any) => (
                  <span key={c.category} className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                    {c.category}: <strong>{c.count}</strong>
                  </span>
                ))}
              </div>
              <div className="max-h-64 overflow-y-auto border border-slate-200 rounded-lg">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-600 sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Word</th>
                      <th className="px-3 py-2">POS Tag</th>
                      <th className="px-3 py-2">Explanation</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {posRes.tokens.map((t: any, i: number) => (
                      <tr key={i}>
                        <td className="px-3 py-1.5 font-mono">{t.word}</td>
                        <td className="px-3 py-1.5 font-semibold text-blue-700">{t.pos_tag} ({t.category})</td>
                        <td className="px-3 py-1.5 text-slate-600">{t.explanation}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {tfidfRes && (
            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">B. TF-IDF Top 10 Terms</h2>
              <p className="text-xs text-slate-500">{tfidfRes.explanation}</p>
              <div className="space-y-2">
                {tfidfRes.top_terms.map((t: any) => (
                  <div key={t.term} className="flex items-center gap-3 text-xs">
                    <span className="w-36 truncate font-mono text-slate-800">{t.term}</span>
                    <div className="flex-1 bg-slate-100 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-teal-600 h-full rounded-full"
                        style={{ width: `${Math.min(100, t.tfidf_score * 160)}%` }}
                      />
                    </div>
                    <span className="w-14 text-right font-mono text-slate-600">{t.tfidf_score}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* C. N-gram Language Model & D. Information Extraction */}
      {(ngramRes || extractRes) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {ngramRes && (
            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">C. N-gram Language Model</h2>
              <p className="text-xs text-slate-500">
                {ngramRes.model_used} &middot; Corpus tokens: {ngramRes.corpus_tokens.toLocaleString()}
              </p>
              <div className="max-h-56 overflow-y-auto border border-slate-200 rounded-lg">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-600 sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Predicted Next Word</th>
                      <th className="px-3 py-2">Count</th>
                      <th className="px-3 py-2">Smoothed P(w|ctx)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {ngramRes.predictions.map((p: any, i: number) => (
                      <tr key={i}>
                        <td className="px-3 py-1.5 font-mono text-blue-700">{p.next_word}</td>
                        <td className="px-3 py-1.5">{p.count}</td>
                        <td className="px-3 py-1.5 font-mono">{p.smoothed_probability}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {extractRes && (
            <div className="card p-5 space-y-3">
              <h2 className="text-sm font-semibold text-slate-900">D. Information Extraction</h2>
              <p className="text-xs text-slate-500">{extractRes.explanation}</p>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="font-semibold text-slate-700 mb-1">Research Methods</div>
                  <div>{extractRes.research_methods.join(", ") || "None detected"}</div>
                </div>
                <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="font-semibold text-slate-700 mb-1">Algorithms</div>
                  <div>{extractRes.algorithms.join(", ") || "None detected"}</div>
                </div>
                <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="font-semibold text-slate-700 mb-1">Technologies</div>
                  <div>{extractRes.technologies.join(", ") || "None detected"}</div>
                </div>
                <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="font-semibold text-slate-700 mb-1">Domains</div>
                  <div>{extractRes.domains.join(", ") || "None detected"}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* E, F, G: WordNet Lexical Semantics, WSD (Lesk), Word Similarity */}
      <div className="card p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">
          E, F, G. WordNet Lexical Semantics, Word Sense Disambiguation (Lesk) &amp; Word Similarity
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">Target Word</label>
            <input
              type="text"
              value={wnWord}
              onChange={(e) => setWnWord(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">Compare Word (Similarity)</label>
            <input
              type="text"
              value={wnCompare}
              onChange={(e) => setWnCompare(e.target.value)}
              className="input-field"
            />
          </div>
          <div className="flex items-end">
            <button onClick={runWordNet} className="btn-primary w-full">
              Analyze in WordNet
            </button>
          </div>
        </div>
        <div>
          <label className="text-xs font-medium text-slate-600 block mb-1">Context Sentence (for Lesk WSD)</label>
          <input
            type="text"
            value={wnSentence}
            onChange={(e) => setWnSentence(e.target.value)}
            className="input-field"
          />
        </div>

        {wnRes && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 pt-2 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1.5">
              <div className="font-semibold text-slate-800">E. Lexical Relationships</div>
              <div><strong>Synonyms:</strong> {wnRes.lexical_semantics.synonyms.join(", ") || "—"}</div>
              <div><strong>Antonyms:</strong> {wnRes.lexical_semantics.antonyms.join(", ") || "—"}</div>
              <div><strong>Hypernyms:</strong> {wnRes.lexical_semantics.hypernyms.join(", ") || "—"}</div>
              <div><strong>Hyponyms:</strong> {wnRes.lexical_semantics.hyponyms.join(", ") || "—"}</div>
            </div>

            {wnRes.word_sense_disambiguation && (
              <div className="p-3.5 bg-blue-50/50 rounded-lg border border-blue-200 space-y-1.5">
                <div className="font-semibold text-blue-900">F. Word Sense Disambiguation</div>
                <div><strong>Predicted Sense:</strong> <span className="font-mono">{wnRes.word_sense_disambiguation.predicted_sense}</span></div>
                <div><strong>Definition:</strong> {wnRes.word_sense_disambiguation.definition}</div>
                <div className="text-slate-600">{wnRes.word_sense_disambiguation.explanation}</div>
              </div>
            )}

            {wnRes.word_similarity && (
              <div className="p-3.5 bg-teal-50/50 rounded-lg border border-teal-200 space-y-1.5">
                <div className="font-semibold text-teal-900">G. Word Similarity</div>
                <div>
                  <strong>Pair:</strong> {wnRes.word_similarity.word1} &harr; {wnRes.word_similarity.word2}
                </div>
                <div><strong>Wu-Palmer Score:</strong> {wnRes.word_similarity.wup_similarity}</div>
                <div><strong>Path Score:</strong> {wnRes.word_similarity.path_similarity}</div>
                <div className="text-slate-600">{wnRes.word_similarity.interpretation}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
