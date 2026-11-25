import React from "react";

const UNIT_MAPPING = [
  { unit: "Unit I", title: "Introduction & Word Analysis", page: "Paper Analyzer", techniques: "Tokenization, Normalization, Stop-words, PorterStemmer, WordNetLemmatizer, BoW, N-grams, Regex, Morphology, FSA/FST" },
  { unit: "Unit II", title: "Syntax, Lexical Semantics & LMs", page: "NLP Lab", techniques: "POS Tagging, TF-IDF, N-gram Language Model, Information Extraction, WordNet Semantics, Lesk WSD, Word Similarity" },
  { unit: "Unit III", title: "Semantic Analysis (Modular)", page: "Semantic Analysis", techniques: "Sentence Similarity, Concept Identification, Contextual Meaning, Semantic Relationships" },
  { unit: "Unit IV", title: "Discourse & Pragmatics", page: "Discourse & Pragmatics", techniques: "Cohesion, Discourse Structure, Adjacency Pairs, Implicature, Grice's Maxims, Deixis, Endophora/Exophora, Speech Acts, Face" },
  { unit: "Unit V", title: "Language Models & Summarization", page: "AI Summarizer", techniques: "Hugging Face Pipeline + Extractive Fallback, Prompt Templates, ROUGE-1/2/L, RNN/Transformer/BERT/GPT/PEFT Concepts" },
];

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="card p-6 space-y-3">
        <h1 className="text-xl font-bold text-slate-900">About ResearchLens</h1>
        <p className="text-sm text-slate-600 leading-relaxed">
          <strong>ResearchLens</strong> is an academic full-stack NLP platform built for the{" "}
          <strong>Natural Language Processing and Language Models (NLPLM)</strong> course. It demonstrates
          practical implementations of concepts across Units I–V using a local synthetic corpus of 210 academic research papers.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <div className="font-semibold text-slate-800">Frontend</div>
            <div className="text-slate-600 mt-0.5">React, TypeScript, Vite, Tailwind CSS, Recharts, React Query, Axios</div>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <div className="font-semibold text-slate-800">Backend &amp; DB</div>
            <div className="text-slate-600 mt-0.5">Python, FastAPI, Uvicorn, Pydantic, SQLAlchemy, SQLite</div>
          </div>
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <div className="font-semibold text-slate-800">NLP Stack</div>
            <div className="text-slate-600 mt-0.5">NLTK, Scikit-learn, Hugging Face Transformers, ROUGE, NumPy, Pandas</div>
          </div>
        </div>
      </div>

      <div className="card p-6 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">NLPLM Syllabus Unit Mapping</h2>
        <div className="overflow-x-auto border border-slate-200 rounded-lg">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600">
              <tr>
                <th className="px-4 py-2.5">Unit</th>
                <th className="px-4 py-2.5">Topic</th>
                <th className="px-4 py-2.5">ResearchLens Page</th>
                <th className="px-4 py-2.5">Implemented Techniques</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {UNIT_MAPPING.map((u) => (
                <tr key={u.unit}>
                  <td className="px-4 py-2.5 font-semibold text-blue-700 whitespace-nowrap">{u.unit}</td>
                  <td className="px-4 py-2.5 font-medium text-slate-900">{u.title}</td>
                  <td className="px-4 py-2.5 text-teal-700 font-medium whitespace-nowrap">{u.page}</td>
                  <td className="px-4 py-2.5 text-slate-600">{u.techniques}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
