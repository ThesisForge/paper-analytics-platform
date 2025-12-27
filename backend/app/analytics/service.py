import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Dict, List
from backend.app.models import models


def analytics_overview(db: Session, month: str):
    start_date = dt.datetime.strptime(month + "-01", "%Y-%m-%d").date()
    end_date = (start_date + dt.timedelta(days=32)).replace(day=1)
    q = db.query(models.Publication).filter(
        models.Publication.published_at >= start_date,
        models.Publication.published_at < end_date,
    )
    total = q.count()
    domain_counts = (
        db.query(models.Publication.domain, func.count(models.Publication.id))
        .filter(models.Publication.published_at >= start_date, models.Publication.published_at < end_date)
        .group_by(models.Publication.domain)
        .all()
    )
    subtopic_counts = (
        db.query(func.unnest(models.Publication.subtopics), func.count(models.Publication.id))
        .filter(models.Publication.published_at >= start_date, models.Publication.published_at < end_date)
        .group_by(func.unnest(models.Publication.subtopics))
        .all()
    )
    source_counts = (
        db.query(models.Publication.source, func.count(models.Publication.id))
        .filter(models.Publication.published_at >= start_date, models.Publication.published_at < end_date)
        .group_by(models.Publication.source)
        .all()
    )
    return {
        "total": total,
        "domains": {k: v for k, v in domain_counts},
        "subtopics": {k: v for k, v in subtopic_counts if k},
        "sources": {k: v for k, v in source_counts},
    }


def top_venues_and_authors(db: Session, month: str):
    start_date = dt.datetime.strptime(month + "-01", "%Y-%m-%d").date()
    end_date = (start_date + dt.timedelta(days=32)).replace(day=1)
    venues = (
        db.query(models.Publication.venue, func.count(models.Publication.id))
        .filter(models.Publication.published_at >= start_date, models.Publication.published_at < end_date)
        .group_by(models.Publication.venue)
        .order_by(func.count(models.Publication.id).desc())
        .limit(5)
        .all()
    )
    authors = (
        db.query(models.Author.name, func.count(models.Publication.id))
        .join(models.PublicationAuthor, models.Author.id == models.PublicationAuthor.author_id)
        .join(models.Publication, models.Publication.id == models.PublicationAuthor.publication_id)
        .filter(models.Publication.published_at >= start_date, models.Publication.published_at < end_date)
        .group_by(models.Author.name)
        .order_by(func.count(models.Publication.id).desc())
        .limit(5)
        .all()
    )
    return {
        "venues": {k: v for k, v in venues if k},
        "authors": {k: v for k, v in authors if k},
    }
