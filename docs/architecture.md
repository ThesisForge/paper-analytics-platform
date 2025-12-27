# Architecture Overview

The platform is a monorepo with FastAPI backend, RQ worker, and React frontend. Ingestion services pull monthly metadata from ArXiv and OpenAlex APIs (no scraping) and persist normalized publications into Postgres. Redis backs RQ queues and rate limiting. Classification uses rule-based keyword detection to assign domain and subtopics.

## Components
- **backend**: FastAPI with SQLAlchemy models, ingestion services, analytics endpoints, metrics, and rate limiting middleware.
- **worker**: RQ worker consuming ingestion jobs. Shares backend code for database models and services.
- **frontend**: Vite + React dashboard offering month/domain filters, KPI cards, and publication list.
- **infra**: docker-compose for local development (Postgres, Redis, backend, worker, frontend).
- **deploy**: Kubernetes manifests (Traefik ingress, PVC-backed Postgres, backend/worker/frontend deployments).

## Data Flow
1. Admin triggers ingestion for a month/source via API or RQ job.
2. Ingestion client fetches from provider, normalizes fields, deduplicates by arXiv ID/DOI/title similarity.
3. Classification assigns domain/subtopics.
4. Raw payload stored for traceability. Analytics endpoints aggregate counts by domain/subtopic/source.
5. Frontend calls analytics APIs to render KPIs and lists.
