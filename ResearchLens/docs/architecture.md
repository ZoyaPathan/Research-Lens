# ResearchLens System Architecture

## Overview

ResearchLens follows a clean 3-tier local architecture:

1. **Presentation Layer (React + TypeScript + Vite)**
   - Single Page Application (SPA) styled with Tailwind CSS.
   - Uses `Axios` (`src/api/client.ts`) and `@tanstack/react-query` for API communication and caching.
   - Uses `Recharts` for interactive analytics charts.

2. **Application & NLP Layer (FastAPI + Python)**
   - RESTful API routers in `backend/app/routers/`.
   - Request/response validation via Pydantic v2 schemas (`backend/app/schemas.py`).
   - Modular NLP services in `backend/app/services/` implementing Units I–V using NLTK, Scikit-learn, Hugging Face Transformers (lazy-loaded with extractive fallback), and `rouge-score`.

3. **Persistence Layer (SQLite + SQLAlchemy)**
   - Local file-based SQLite database (`backend/researchlens.db`).
   - Auto-seeded on FastAPI startup if empty via `backend/app/utils/dataset_loader.py` from `backend/data/research_papers.json`.
