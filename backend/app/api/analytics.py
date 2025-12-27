from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.analytics.service import analytics_overview, top_venues_and_authors
from backend.app.db.session import get_db
from backend.app.schemas.publication import Publication
from backend.app.models import models

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview/{month}")
def overview(month: str, db: Session = Depends(get_db)):
    return analytics_overview(db, month)


@router.get("/top/{month}")
def top_lists(month: str, db: Session = Depends(get_db)):
    return top_venues_and_authors(db, month)


@router.get("/publications/{month}", response_model=list[Publication])
def list_publications(month: str, db: Session = Depends(get_db)):
    start_date = f"{month}-01"
    pubs = db.query(models.Publication).filter(models.Publication.published_at >= start_date).all()
    return pubs
