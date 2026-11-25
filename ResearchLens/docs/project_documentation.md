# ResearchLens Project Documentation

## 1. Academic Context
ResearchLens was developed for the **Natural Language Processing and Language Models (NLPLM)** university course. Its primary objective is to bridge theoretical NLP concepts across Units I–V with an interactive, locally runnable full-stack web application.

## 2. Design Principles
- **Zero Paid APIs**: All NLP operations execute locally without OpenAI or external cloud APIs.
- **Graceful Degradation**: Every optional external resource (NLTK WordNet/taggers, Hugging Face summarization models, spaCy) has a documented, working local fallback so the application never crashes on a fresh environment.
- **Academic Clarity**: Heuristic modules (such as Unit IV discourse/pragmatics and Unit I FSA/FST) explicitly display their educational scope and limitations.
