# RAG Standard Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the existing Streamlit PDF RAG prototype into `AIProjects/Project001_RAGBotStandard` and keep all related project content inside that numbered project folder.

**Architecture:** Keep Streamlit as the UI entrypoint and move reusable RAG logic into small modules under `rag_bot/`. Use HuggingFace embeddings with Chroma for local PDF retrieval, and keep generated data under `data/`.

**Tech Stack:** Python 3.11, Streamlit, LangChain, Chroma, HuggingFace sentence transformers, pypdf, pytest.

---

### Task 1: Project Skeleton

**Files:**
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/.gitignore`
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/README.md`
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/requirements.txt`
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/pyproject.toml`

- [x] **Step 1: Create a clean Python project root**

Create documentation, dependency metadata, and ignore rules so `.venv`, Chroma data, Python cache files, and uploaded PDFs are not treated as source.

- [x] **Step 2: Keep runtime instructions explicit**

Document environment creation, dependency installation, and Streamlit startup commands in `README.md`.

### Task 2: Application Modules

**Files:**
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/app.py`
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/rag_bot/__init__.py`
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/rag_bot/pdf_loader.py`
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/rag_bot/vectorstore.py`

- [x] **Step 1: Migrate PDF reading and text splitting**

Move PDF extraction into `app/pdf_loader.py` and split extracted text into chunks before indexing.

- [x] **Step 2: Migrate vectorstore creation**

Move Chroma/HuggingFace setup into `app/vectorstore.py` and return a retriever-compatible vector store.

- [x] **Step 3: Keep Streamlit order safe**

Make `app.py` create the vectorstore only after files are uploaded, then query it only after a question exists.

### Task 3: Verification

**Files:**
- Create: `AIProjects/Project001_RAGBotStandard/02_Source/rag-bot-standard/tests/test_pdf_loader.py`

- [x] **Step 1: Add a small unit test**

Test the text chunking behavior without needing a live Streamlit browser.

- [x] **Step 2: Run syntax checks**

Run Python compile checks across the new project.
