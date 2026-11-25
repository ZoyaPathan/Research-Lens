import React, { useState } from "react";
import { GitBranch } from "lucide-react";
import { api } from "../api/client";

export const SemanticPage: React.FC = () => {
  const [sentence1, setSentence1] = useState(
    "Deep learning models improve medical image segmentation accuracy in clinical diagnosis."
  );
  const [sentence2, setSentence2] = useState(
    "Neural networks enhance diagnostic accuracy for clinical medical imaging tasks."
  );
  const [simRes, setSimRes] = useState<any>(null);

  const [abstractText, setAbstractText] = useState(
    "Federated learning enables privacy-preserving healthcare diagnostics across distributed hospital registries without sharing raw patient data."
  );
  const [targetWord, setTargetWord] = useState("learning");
  const [semRes, setSemRes] = useState<any>(null);
  const [error, setError] = useState("");

  const compareSentences = async () => {
    setError("");
    try {
      const data = await api.semanticSimilarity(sentence1, sentence2, "auto");
      setSimRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Similarity comparison failed.");
    }
  };

  const analyzeConcepts = async () => {
    setError("");
    try {
      const data = await api.semanticAnalyze(abstractText, targetWord);
      setSemRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Semantic analysis failed.");
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <span className="text-xs font-semibold uppercase tracking-wider text-teal-700">Unit III (Modular)</span>
        <h1 className="text-xl font-bold text-slate-900">Semantic Analysis</h1>
        <p className="text-sm text-slate-600 mt-1">
          Modular educational semantic-analysis module covering sentence similarity, concept identification, contextual meaning, and semantic relationships.
        </p>
      </div>

      {error && <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">{error}</div>}

      {/* Sentence-Level Semantic Comparison */}
      <div className="card p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">A &amp; E. Sentence-Level Semantic Similarity</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">Sentence 1</label>
            <textarea
              rows={3}
              value={sentence1}
              onChange={(e) => setSentence1(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-600 block mb-1">Sentence 2</label>
            <textarea
              rows={3}
              value={sentence2}
              onChange={(e) => setSentence2(e.target.value)}
              className="input-field"
            />
          </div>
        </div>
        <div className="flex justify-end">
          <button onClick={compareSentences} className="btn-primary">
            <GitBranch className="w-4 h-4" /> Compare Semantic Similarity
          </button>
        </div>

        {simRes && (
          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2 text-xs">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="font-semibold text-slate-800">Method: {simRes.method_used}</span>
              <span className="px-3 py-1 rounded-full bg-teal-100 text-teal-900 font-bold text-sm">
                {simRes.similarity_percentage}% Similarity (Score: {simRes.similarity_score})
              </span>
            </div>
            <div>
              <strong>Matching Concepts:</strong>{" "}
              {simRes.matching_concepts.length ? simRes.matching_concepts.join(", ") : "None"}
            </div>
            <p className="text-slate-600">{simRes.explanation}</p>
          </div>
        )}
      </div>

      {/* Concept Identification & Contextual Meaning */}
      <div className="card p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">
          B, C, D. Keyword &amp; Concept Identification, Contextual Meaning &amp; Relationships
        </h2>
        <textarea
          rows={3}
          value={abstractText}
          onChange={(e) => setAbstractText(e.target.value)}
          className="input-field"
        />
        <div className="flex flex-col sm:flex-row gap-3 items-end">
          <div className="flex-1">
            <label className="text-xs font-medium text-slate-600 block mb-1">Target Word for Contextual Meaning</label>
            <input
              type="text"
              value={targetWord}
              onChange={(e) => setTargetWord(e.target.value)}
              className="input-field"
            />
          </div>
          <button onClick={analyzeConcepts} className="btn-primary">
            Analyze Concepts &amp; Meaning
          </button>
        </div>

        {semRes && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 text-xs pt-2">
            <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1.5">
              <div className="font-semibold text-slate-800">Identified Concepts</div>
              <div><strong>Main Topic:</strong> {semRes.concept_identification.main_research_topic}</div>
              <div><strong>Technical Concepts:</strong> {semRes.concept_identification.technical_concepts.join(", ") || "—"}</div>
              <div><strong>Methods:</strong> {semRes.concept_identification.methods.join(", ") || "—"}</div>
              <div><strong>Applications:</strong> {semRes.concept_identification.applications.join(", ") || "—"}</div>
            </div>

            {semRes.contextual_meaning && (
              <div className="p-3.5 bg-blue-50/50 rounded-lg border border-blue-200 space-y-1.5">
                <div className="font-semibold text-blue-900">Contextual Meaning ({semRes.contextual_meaning.target_word})</div>
                <div><strong>Sense:</strong> <span className="font-mono">{semRes.contextual_meaning.predicted_sense}</span></div>
                <div><strong>Definition:</strong> {semRes.contextual_meaning.definition}</div>
              </div>
            )}

            <div className="p-3.5 bg-teal-50/50 rounded-lg border border-teal-200 space-y-1.5">
              <div className="font-semibold text-teal-900">Semantic Relationships</div>
              <div><strong>Synonyms:</strong> {semRes.semantic_relationships.synonyms.join(", ") || "—"}</div>
              <div><strong>Hypernyms:</strong> {semRes.semantic_relationships.hypernyms.join(", ") || "—"}</div>
              <div><strong>Hyponyms:</strong> {semRes.semantic_relationships.hyponyms.join(", ") || "—"}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
