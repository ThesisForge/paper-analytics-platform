import datetime as dt
from typing import List
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, UniqueConstraint, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from backend.app.db.session import Base


class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    abstract = Column(Text)
    venue = Column(String(255))
    categories = Column(ARRAY(String), default=list)
    arxiv_id = Column(String(50), unique=True, nullable=True)
    doi = Column(String(255), unique=True, nullable=True)
    source = Column(String(50), nullable=False)
    url = Column(String(500))
    published_at = Column(Date, nullable=False)
    domain = Column(String(100), default="Other")
    subtopics = Column(ARRAY(String), default=list)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    authors = relationship("Author", secondary="publication_authors", back_populates="publications")
    raw_payloads = relationship("RawPayload", back_populates="publication")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    publications = relationship("Publication", secondary="publication_authors", back_populates="authors")


class PublicationAuthor(Base):
    __tablename__ = "publication_authors"
    publication_id = Column(Integer, ForeignKey("publications.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)


class RawPayload(Base):
    __tablename__ = "raw_payloads"
    id = Column(Integer, primary_key=True, index=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=False)
    source = Column(String(50), nullable=False)
    external_id = Column(String(255))
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    publication = relationship("Publication", back_populates="raw_payloads")


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False)
    month = Column(String(7), nullable=False)
    status = Column(String(50), default="pending")
    started_at = Column(DateTime, default=dt.datetime.utcnow)
    finished_at = Column(DateTime)
    summary = Column(JSON, default=dict)

    __table_args__ = (UniqueConstraint("source", "month", name="uq_source_month"),)
