# ResearchLens

**An NLP-Based Academic Research Paper Analysis, Semantic Search and Summarization Platform**

---

## 1. Project Introduction

ResearchLens is an academic full-stack web application built for the **Natural Language Processing and Language Models (NLPLM)** course. It combines a React + TypeScript dashboard with a FastAPI + SQLite backend and real NLP pipelines (NLTK, Scikit-learn, Hugging Face Transformers, ROUGE) to analyze, search, and summarize a corpus of 210 synthetic academic research papers across 7 domains.

## 2. Problem Statement

Students and researchers often struggle to discover relevant academic research papers, understand lengthy abstracts, identify important research concepts, and find connections between different studies. ResearchLens addresses this by providing interactive keyword and TF-IDF semantic search, linguistic preprocessing, syntactic/lexical analysis, discourse and pragmatic demonstrations, and automated summarization with ROUGE evaluation.

## 3. Project Objectives

- Build an intuitive, responsive research analytics dashboard backed by SQLite.
- Implement and visibly demonstrate NLP techniques from **Units I–V** of the NLPLM syllabus.
- Provide local, zero-cost execution with no paid API keys required.
- Integrate Hugging Face Transformers summarization lazily with a deterministic extractive fallback.

## 4. Features

- **Dashboard**: Real-time corpus metrics, domain distribution chart, publication year chart, recent papers, and frequent keywords.
- **Research Explorer**: Browse 210 synthetic papers with title/keyword search, domain and year filters, sorting, pagination, and detail modal.
- **Smart Search**: Keyword search and TF-IDF + Cosine Similarity ranked retrieval with matching keywords and relevance scores.
- **Paper Analyzer (Unit I)**: Tokenization, normalization, stop-word removal, Porter stemming, WordNet lemmatization, Bag of Words, N-grams, regex extraction, morphological analysis, and educational FSA/FST demos.
- **NLP Lab (Unit II)**: POS tagging, TF-IDF top terms, N-gram language model probabilities, information extraction, WordNet lexical relations, Lesk WSD, and WordNet word similarity.
- **Semantic Analysis (Unit III – Modular)**: Sentence-level semantic similarity, concept identification, contextual meaning, and semantic relationships.
- **Discourse & Pragmatics (Unit IV)**: Cohesion, heuristic discourse structure, adjacency pairs, implicature, Grice's maxims, deixis, endophora/exophora, speech acts, and pragmatic markers & face theory.
- **AI Summarizer (Unit V)**: Lazy-loaded Hugging Face pipeline with extractive fallback, 5 prompt engineering templates, ROUGE-1/2/L evaluation, and LLM concepts guide.
- **Research Insights**: Interactive Recharts visualizations of domains, years, keywords, methodologies, and abstract lengths.

## 5. Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, React Router, Axios, TanStack React Query, Recharts, Lucide React.
- **Backend**: Python, FastAPI, Uvicorn, Pydantic, SQLAlchemy.
- **NLP Libraries**: NLTK, Scikit-learn, Hugging Face Transformers, `rouge-score`, NumPy, Pandas.
- **Database**: SQLite (`researchlens.db`).

## 6. Architecture

The React SPA communicates over HTTP/JSON with FastAPI routers via a centralized Axios client (`/api/*`). FastAPI delegates NLP processing to modular services in `backend/app/services/` and persists papers and analysis logs in SQLite via SQLAlchemy. See [docs/architecture.md](docs/architecture.md) for details.

## 7. Folder Structure

```text
ResearchLens/
├── frontend/
│   ├── src/
│   │   ├── api/client.ts
│   │   ├── components/
│   │   ├── pages/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── data/
│   │   ├── research_papers.csv
│   │   └── research_papers.json
│   ├── scripts/
│   │   ├── generate_dataset.py
│   │   └── seed_database.py
│   ├── tests/
│   │   └── test_api.py
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── architecture.md
│   ├── api_documentation.md
│   ├── nlplm_unit_mapping.md
│   └── project_documentation.md
├── .gitignore
└── README.md
```

## 8. Database Details

SQLite database (`backend/researchlens.db`) with two tables:
- `research_papers`: `id`, `paper_id` (unique), `title`, `abstract`, `authors`, `research_domain`, `keywords`, `methodology`, `publication_year`, `created_at`.
- `analysis_logs`: `id`, `paper_id`, `module_name`, `created_at`.

## 9. Dataset Information

210 original synthetic academic research papers (30 per domain across 7 domains: AI & ML, NLP, Computer Vision, Edge Computing & IoT, Cybersecurity, Data Science, Cloud Computing) spanning 2020–2026, stored in `backend/data/research_papers.csv` and `backend/data/research_papers.json`.

## 10. NLP Techniques Implemented

Tokenization, normalization, stop-word filtering, Porter stemming, WordNet lemmatization, Bag of Words (`CountVectorizer`), N-gram frequency & language modeling, regex pattern extraction, inflectional/derivational morphology, educational FSA/FST, POS tagging, TF-IDF cosine similarity, rule-based NER/IE, WordNet lexical semantics, Lesk WSD, Wu-Palmer similarity, heuristic discourse/pragmatics, Hugging Face/extractive summarization, and ROUGE evaluation.

## 11. Unit-Wise NLPLM Mapping

See [docs/nlplm_unit_mapping.md](docs/nlplm_unit_mapping.md) for the complete syllabus-to-implementation evaluation table.

## 12. Installation Instructions

Prerequisites: Python 3.10+ and Node.js 18+.

## 13. Backend Setup

```powershell
cd ResearchLens\backend
python -m pip install -r requirements.txt
python -c "import nltk; [nltk.download(p) for p in ['punkt','punkt_tab','stopwords','wordnet','omw-1.4','averaged_perceptron_tagger','averaged_perceptron_tagger_eng']]"
python scripts\seed_database.py
```

## 14. Frontend Setup

```powershell
cd ResearchLens\frontend
npm install
```

## 15. How to Run the Project

1. **Start Backend** (Terminal 1):
   ```powershell
   cd ResearchLens\backend
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
2. **Start Frontend** (Terminal 2):
   ```powershell
   cd ResearchLens\frontend
   npm run dev
   ```
3. Open `http://localhost:5173` in your browser. Swagger API docs are at `http://127.0.0.1:8000/docs`.

## 16. API Documentation

See [docs/api_documentation.md](docs/api_documentation.md) or visit `/docs` when FastAPI is running.

## 17. Troubleshooting

- **Missing NLTK data**: Run the NLTK download command in Section 13. The backend also includes graceful rule-based fallbacks if a corpus is missing.
- **Hugging Face model download**: If `sshleifer/distilbart-cnn-12-6` or PyTorch is not installed/downloaded, the AI Summarizer automatically uses the local TF-IDF extractive fallback.
- **Port conflicts**: Ensure ports `8000` (FastAPI) and `5173` (Vite) are free.

## 18. Limitations

- Unit III is implemented as a modular semantic-analysis module pending detailed syllabus confirmation.
- Unit IV discourse and pragmatics demonstrations use transparent rule-based heuristics and do not provide human-level pragmatic reasoning.
- Finite Automata / FST demonstrations are educational examples rather than full morphological transducers.
- Synthetic dataset abstracts are template-generated for academic demonstration.

## 19. Future Scope

- Integrating dense sentence-transformer embeddings (`all-MiniLM-L6-v2`) when PyTorch is available.
- Supporting PDF upload and parsing for real user-uploaded papers.
- Expanding Unit III modules once detailed syllabus topics are finalized.
