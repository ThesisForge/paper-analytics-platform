import datetime as dt
import logging
from difflib import SequenceMatcher
from typing import Dict, List
from sqlalchemy.orm import Session

from backend.app.ingestion.arxiv import fetch_arxiv_by_month
from backend.app.ingestion.openalex import fetch_openalex_by_month
from backend.app.models import models
from backend.app.classifiers.rules import classify_text

logger = logging.getLogger(__name__)


class IngestionService:
    SOURCES = {
        "arxiv": fetch_arxiv_by_month,
        "openalex": fetch_openalex_by_month,
    }

    def __init__(self, db: Session):
        self.db = db

    def trigger(self, source: str, month: str) -> models.IngestionRun:
        fetcher = self.SOURCES.get(source)
        if not fetcher:
            raise ValueError("Unknown source")
        run = models.IngestionRun(source=source, month=month, status="running")
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        added, skipped = 0, 0
        for item in fetcher(month):
            if self._deduplicate(item):
                skipped += 1
                continue
            pub = self._create_publication(item, source)
            self.db.add(pub)
            self.db.commit()
            self.db.refresh(pub)
            added += 1
        run.status = "completed"
        run.finished_at = dt.datetime.utcnow()
        run.summary = {"added": added, "skipped": skipped}
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def _deduplicate(self, item: Dict) -> bool:
        arxiv_id = item.get("arxiv_id")
        doi = item.get("doi")
        title = item.get("title", "")
        if arxiv_id and self.db.query(models.Publication).filter_by(arxiv_id=arxiv_id).first():
            logger.info("Duplicate arXiv id %s", arxiv_id)
            return True
        if doi and self.db.query(models.Publication).filter_by(doi=doi).first():
            logger.info("Duplicate DOI %s", doi)
            return True
        existing = self.db.query(models.Publication).all()
        for pub in existing:
            ratio = SequenceMatcher(None, pub.title.lower(), title.lower()).ratio()
            if ratio > 0.95:
                logger.info("Duplicate by title similarity: %s", title)
                return True
        return False

    def _create_publication(self, item: Dict, source: str) -> models.Publication:
        authors = item.get("authors", [])
        author_entities = []
        for name in authors:
            if not name:
                continue
            existing = self.db.query(models.Author).filter_by(name=name).first()
            if existing:
                author_entities.append(existing)
            else:
                new_author = models.Author(name=name)
                self.db.add(new_author)
                self.db.commit()
                self.db.refresh(new_author)
                author_entities.append(new_author)

        text = f"{item.get('title','')} {item.get('abstract','')}"
        domain, subtopics = classify_text(text)
        pub = models.Publication(
            title=item.get("title"),
            abstract=item.get("abstract") if not isinstance(item.get("abstract"), dict) else " ".join(item.get("abstract", {}).keys()),
            venue=item.get("venue"),
            categories=[c.get("term", c) if isinstance(c, dict) else c for c in item.get("categories", [])],
            arxiv_id=item.get("arxiv_id"),
            doi=item.get("doi"),
            source=source,
            url=item.get("url"),
            published_at=dt.datetime.fromisoformat(str(item.get("published"))).date(),
            domain=domain,
            subtopics=subtopics,
        )
        pub.authors = author_entities

        payload = models.RawPayload(
            publication=pub,
            source=source,
            external_id=item.get("arxiv_id") or item.get("doi") or item.get("url"),
            payload=item.get("raw", {}),
        )
        self.db.add(payload)
        return pub
