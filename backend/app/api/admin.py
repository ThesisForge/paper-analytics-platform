from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.api.deps import get_api_key
from backend.app.db.session import get_db
from backend.app.services.ingestion_service import IngestionService
from backend.app.schemas.publication import IngestionRun

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ingest/{source}/{month}", response_model=IngestionRun)
def trigger_ingestion(source: str, month: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    service = IngestionService(db)
    run = service.trigger(source, month)
    return run


@router.get("/runs", response_model=list[IngestionRun])
def list_runs(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    from backend.app.models import models

    runs = db.query(models.IngestionRun).order_by(models.IngestionRun.started_at.desc()).limit(50).all()
    return runs
