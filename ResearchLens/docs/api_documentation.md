# ResearchLens API Documentation

Base URL: `http://127.0.0.1:8000`  
Interactive Swagger UI: `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check and NLTK resource availability status. |
| `GET` | `/api/papers` | Paginated list of research papers with `search`, `domain`, `year`, and `sort` query params. |
| `GET` | `/api/papers/{paper_id}` | Retrieve a single research paper by its `paper_id`. |
| `GET` | `/api/domains` | List distinct research domains with counts and available publication years. |
| `GET` | `/api/search` | Smart search (`q`, `mode=hybrid\|keyword`, `top_k`) using TF-IDF cosine similarity + keyword boost. |
| `POST` | `/api/analyze` | Unit I full analysis (tokenization, normalization, stop-words, stemming, lemmatization, BoW, n-grams, regex, morphology, FSA/FST). |
| `POST` | `/api/nlp/pos-tag` | Unit II POS tagging with category distribution and explanations. |
| `POST` | `/api/nlp/tfidf` | Unit II TF-IDF top-K important terms for text or `paper_id`. |
| `POST` | `/api/nlp/ngrams` | Unit II N-gram language model probabilities for a given `context` and `n`. |
| `POST` | `/api/nlp/extract` | Unit II information extraction (methods, algorithms, technologies, domains). |
| `POST` | `/api/nlp/wordnet` | Unit II WordNet lexical relations, Lesk WSD, and Wu-Palmer / path word similarity. |
| `POST` | `/api/semantic/similarity` | Unit III sentence-level semantic similarity comparison. |
| `POST` | `/api/semantic/analyze` | Unit III concept identification, contextual meaning, and semantic relationships. |
| `POST` | `/api/discourse/analyze` | Unit IV discourse cohesion, heuristic structure, deixis, endophora, speech acts, pragmatic markers. |
| `POST` | `/api/discourse/conversation` | Unit IV adjacency pairs, implicature heuristics, and Grice's Cooperative Principle. |
| `GET` | `/api/summarize/status` | Unit V Hugging Face summarization model loading status. |
| `POST` | `/api/summarize` | Unit V text summarization with length, prompt instruction template, and HF/extractive fallback. |
| `POST` | `/api/summarize/evaluate` | Unit V ROUGE-1, ROUGE-2, and ROUGE-L evaluation against a reference summary. |
| `GET` | `/api/insights/overview` | Aggregated corpus statistics, domain/year distributions, top keywords, methods, and abstract lengths. |
| `GET` | `/api/insights/domains` | Paper counts grouped by research domain. |
| `GET` | `/api/insights/keywords` | Top 25 most frequent keywords across the corpus. |
