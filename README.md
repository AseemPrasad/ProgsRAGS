# ProgsRAGS — Trust-Aware Knowledge Retrieval Prototype

ProgsRAGS is a **research-oriented prototype** exploring how to make Retrieval-Augmented Generation (RAG) systems *safer, more trustworthy, and more defensible* for organizational knowledge use.

Most RAG systems optimize for recall and fluency.  
This project instead prioritizes **correctness, uncertainty, and auditability**.

> The core idea:  
> **If the system cannot support an answer with sufficient evidence, it should refuse to answer.**

This is not a chatbot.  
It is a minimal example of **trust-aware knowledge infrastructure**.

---

## Problem Motivation

Modern organizations struggle to reliably answer questions about their own knowledge:

- Documents conflict with each other
- Policies change over time, but old versions persist
- Answers are given confidently without sufficient evidence
- Users are forced to manually double-check AI outputs
- Institutional knowledge degrades as people leave

Most RAG demos fail because they:
- Treat retrieved text as ground truth
- Hide uncertainty
- Ignore time and document conflicts
- Optimize for “answering” instead of “being correct”

This project explores a different approach.

---

## Design Principles

These principles are enforced structurally, not just conceptually:

- **No Answer Without Evidence**
- **“I Don’t Know” Is a Valid Outcome**
- **Newer Knowledge > Older Knowledge**
- **Conflicts Must Be Explicit**
- **Trust > Recall**
- **Metadata Is First-Class**

---
## System Architecture

Ingestion Layer: Multi-source ingestion (PDF, Google Drive) with deterministic chunking and metadata extraction (Author, Timestamp, Version).

Knowledge Store: A dual-storage strategy using PostgreSQL for relational metadata/audit logs and Qdrant for vector embeddings.

The Trust Gate: A proprietary heuristic layer that evaluates retrieved chunks for relevance, freshness, and temporal conflicts before passing them to the LLM.

Reasoning Layer: A citation-constrained LLM interface (currently stubbed for architectural demo) that generates answers strictly from provided context.

User Experience: A Svelte-based interface that displays answers alongside confidence indicators and conflict warnings.


## Key Features

### Ingestion
- PDF upload (Google Drive read-only supported in MVP)
- Deterministic text chunking
- Metadata extraction (source, timestamp, document ID)
- Separation of metadata (Postgres) and embeddings (Qdrant)

### Retrieval & Trust Gate (Core Innovation)
Before any answer is generated, retrieved chunks are evaluated for:
- **Relevance**
- **Freshness**
- **Conflicts**
- **Sufficiency**

If evidence is weak, outdated, or contradictory, the system **blocks generation** and returns an explicit refusal.

### Reasoning Layer
- Answers must be grounded in retrieved sources
- Each claim must be traceable to evidence
- Conflicts are surfaced explicitly
- Confidence level reflects evidence quality

(LLM calls are intentionally mocked in this prototype to focus on system design.)

### Observability
- Query logs
- Blocked answers
- Detected conflicts
- Repeated unanswered questions

These metrics are treated as **product signals**, not just logs.

---

## What This Project Is / Is Not

**This is:**
- A trust-aware RAG prototype
- A system design exploration
- A correctness-first alternative to naive RAG

**This is not:**
- An enterprise-ready product
- A chatbot
- A generic “chat with your PDF” demo
- A solution to all hallucinations

---

## Tech Stack

**Backend**
- Python, FastAPI
- Async SQLAlchemy + PostgreSQL
- Qdrant (vector database)

**Frontend**
- Svelte + Vite

**AI (intentionally mocked in MVP)**
- Embeddings: OpenAI-compatible interface
- LLM: citation-constrained prompt design

**Infrastructure Orchestrated**
- Docker Compose for local services

---

## Why This Matters

This project demonstrates that:
- Hallucination is often a *systems problem*, not a model problem
- Trust can be enforced *before* generation
- Refusal paths are a feature, not a failure
- Metadata and time-awareness are essential for real-world knowledge systems
