"""Pytest suite for ResearchLens FastAPI endpoints and NLP services (in-process ASGI)."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import httpx

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import Base, SessionLocal, engine
from app.main import app
from app.utils.dataset_loader import seed_papers_if_empty


def _ensure_seeded():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_papers_if_empty(db)
    finally:
        db.close()


async def _run_all_checks():
    _ensure_seeded()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health
        res = await client.get("/api/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

        # 2. Papers & Domains
        res = await client.get("/api/papers?page=1&page_size=10")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 210
        assert len(data["items"]) == 10
        first_id = data["items"][0]["paper_id"]

        detail = await client.get(f"/api/papers/{first_id}")
        assert detail.status_code == 200
        assert detail.json()["paper_id"] == first_id

        domains = await client.get("/api/domains")
        assert domains.status_code == 200
        assert len(domains.json()["domains"]) == 7

        # 3. Smart Search
        search = await client.get("/api/search?q=machine+learning+healthcare")
        assert search.status_code == 200
        assert search.json()["total_results"] > 0
        assert search.json()["results"][0]["relevance_score"] > 0

        # 4. Unit I Analyzer
        ana = await client.post("/api/analyze", json={
            "text": "In 2025, federated learning models improved clinical diagnostics by 14.5%. Contact research@example.org for datasets."
        })
        assert ana.status_code == 200
        ad = ana.json()
        assert ad["tokenization"]["total_token_count"] > 10
        assert len(ad["stemming"]["rows"]) > 0
        assert len(ad["lemmatization"]["rows"]) > 0
        assert "research@example.org" in ad["regex"]["emails"]
        assert "2025" in ad["regex"]["years"]

        # 5. Unit II NLP Lab
        sample = "Deep neural networks learn hierarchical representations for medical imaging."
        pos = await client.post("/api/nlp/pos-tag", json={"text": sample})
        assert pos.status_code == 200
        assert pos.json()["total_tagged_tokens"] > 5

        tfidf = await client.post("/api/nlp/tfidf", json={"text": sample, "top_k": 5})
        assert tfidf.status_code == 200
        assert len(tfidf.json()["top_terms"]) > 0

        ngrams = await client.post("/api/nlp/ngrams", json={"context": "deep learning", "n": 2})
        assert ngrams.status_code == 200
        assert ngrams.json()["corpus_tokens"] > 100

        ext = await client.post("/api/nlp/extract", json={"text": "We use Federated Learning and Transformer models with Kubernetes."})
        assert ext.status_code == 200
        assert "federated learning" in ext.json()["research_methods"]

        wn = await client.post("/api/nlp/wordnet", json={"word": "bank", "sentence": "I deposited money at the bank.", "compare_word": "institution"})
        assert wn.status_code == 200
        assert wn.json()["word_sense_disambiguation"] is not None
        assert wn.json()["word_similarity"] is not None

        # 6. Unit III Semantic Analysis
        sim = await client.post("/api/semantic/similarity", json={
            "sentence1": "Deep learning improves medical image segmentation.",
            "sentence2": "Neural networks enhance clinical imaging accuracy.",
        })
        assert sim.status_code == 200
        assert 0.0 <= sim.json()["similarity_score"] <= 1.0

        sem = await client.post("/api/semantic/analyze", json={
            "text": "Federated learning enables privacy-preserving healthcare diagnostics across hospitals.",
            "target_word": "learning",
        })
        assert sem.status_code == 200
        assert "concept_identification" in sem.json()

        # 7. Unit IV Discourse & Pragmatics
        disc = await client.post("/api/discourse/analyze", json={
            "text": "However, existing models struggle with scalability. Therefore, we propose a quantized framework. Experimental results demonstrate a 25% improvement."
        })
        assert disc.status_code == 200
        assert len(disc.json()["discourse_structure"]) == 3

        conv = await client.post("/api/discourse/conversation", json={
            "conversation": "Person A: Are you coming to the meeting?\nPerson B: I have an examination tomorrow."
        })
        assert conv.status_code == 200
        assert len(conv.json()["adjacency_pairs"]) == 1
        assert len(conv.json()["implicatures"]) == 1

        # 8. Unit V Summarizer & ROUGE
        summ = await client.post("/api/summarize", json={
            "text": (
                "Research in natural language processing increasingly demands robust solutions for abstractive summarization. "
                "However, existing approaches struggle with factual consistency on long documents. "
                "We propose a retrieval-augmented transformer architecture. "
                "Experimental results demonstrate a 5.2 point ROUGE-L improvement."
            ),
            "length": "short",
            "instruction": "researcher",
            "use_hf": False,
        })
        assert summ.status_code == 200
        assert len(summ.json()["summary"]) > 10

        ev = await client.post("/api/summarize/evaluate", json={
            "generated_summary": "We propose a retrieval-augmented transformer architecture that improves ROUGE-L.",
            "reference_summary": "A retrieval-augmented transformer architecture improves ROUGE-L on long documents.",
        })
        assert ev.status_code == 200
        assert ev.json()["rouge1"]["fmeasure"] > 0

        # 9. Insights
        ov = await client.get("/api/insights/overview")
        assert ov.status_code == 200
        assert ov.json()["total_papers"] == 210

        dom = await client.get("/api/insights/domains")
        assert dom.status_code == 200
        assert len(dom.json()["domains"]) == 7

        kw = await client.get("/api/insights/keywords")
        assert kw.status_code == 200
        assert kw.json()["total_unique_keywords"] > 20


def test_full_api_integration():
    asyncio.run(_run_all_checks())
