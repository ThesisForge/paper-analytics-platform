# Paper Analytics Platform

Monorepo providing ingestion, classification, and analytics for scientific publications from ArXiv and OpenAlex.

## Quickstart (docker-compose)
```bash
cd infra
docker-compose up --build
```
Backend on `http://localhost:8000`, frontend on `http://localhost:4173`.

Run migrations inside backend container or locally:
```bash
docker-compose run backend alembic -c backend/migrations/alembic.ini upgrade head
```

## Local development
- Python 3.11, Node 20
- Install backend deps: `pip install -r backend/requirements.txt`
- Start API: `uvicorn backend.app.main:app --reload`
- Frontend: `cd frontend && npm install && npm run dev`

## k3s deployment
Apply secrets and storage:
```bash
kubectl apply -f deploy/k8s/secrets.yaml
kubectl apply -f deploy/k8s/data.yaml
```
Build and load images to cluster (e.g., using k3s with local registry) then deploy:
```bash
kubectl apply -f deploy/k8s/backend.yaml
kubectl apply -f deploy/k8s/worker.yaml
kubectl apply -f deploy/k8s/frontend.yaml
kubectl apply -f deploy/k8s/ingress.yaml
```
Traefik ingress expects host `papers.local`.

## Feature flags
- Optional third-party scholar adapters should be wired behind env vars before enabling; none enabled by default.

## Admin API
- Trigger ingestion: `POST /api/admin/ingest/{source}/{month}` with header `x-api-key`
- List runs: `GET /api/admin/runs`

## Analytics API
- Overview: `GET /api/analytics/overview/{month}`
- Top lists: `GET /api/analytics/top/{month}`
- Publications: `GET /api/analytics/publications/{month}`

## Classification
Rule-based keyword classifier assigns domain and subtopics. Extend `backend/app/classifiers/rules.py` for new labels or plug ML/LLM.

## Metrics & Rate limiting
- Prometheus metrics available at `/metrics` when enabled.
- Redis-backed simple rate limiter in middleware.
