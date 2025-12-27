from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class PublicationBase(BaseModel):
    title: str
    abstract: Optional[str]
    venue: Optional[str]
    categories: List[str] = []
    arxiv_id: Optional[str]
    doi: Optional[str]
    source: str
    url: Optional[str]
    published_at: date
    domain: str = "Other"
    subtopics: List[str] = []


class Publication(PublicationBase):
    id: int
    authors: List[Author] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PublicationCreate(PublicationBase):
    authors: List[str] = []
    raw_payload: dict
    external_id: Optional[str]
    source: str


class IngestionRun(BaseModel):
    id: int
    source: str
    month: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime]
    summary: dict

    class Config:
        orm_mode = True
