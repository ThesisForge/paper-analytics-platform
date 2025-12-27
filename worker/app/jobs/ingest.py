import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.services.ingestion_service import IngestionService
from backend.app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)


def ingest(source: str, month: str):
    db = SessionLocal()
    try:
        service = IngestionService(db)
        return service.trigger(source, month)
    finally:
        db.close()
