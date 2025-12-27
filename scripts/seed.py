import os
from backend.app.db.session import SessionLocal
from backend.app.services.ingestion_service import IngestionService


def run():
    db = SessionLocal()
    try:
        service = IngestionService(db)
        service.trigger("arxiv", "2024-01")
        service.trigger("openalex", "2024-01")
    finally:
        db.close()


if __name__ == "__main__":
    run()
