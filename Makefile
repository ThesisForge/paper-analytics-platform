.PHONY: backend frontend worker migrate

backend:
uvicorn backend.app.main:app --reload

frontend:
cd frontend && npm install && npm run dev -- --host 0.0.0.0

worker:
cd worker && python app/worker.py

migrate:
alembic -c backend/migrations/alembic.ini upgrade head
