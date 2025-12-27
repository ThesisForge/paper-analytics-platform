import datetime as dt
import logging
from typing import Dict, List
import requests

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def fetch_openalex_by_month(month: str) -> List[Dict]:
    start_date = dt.datetime.strptime(month + "-01", "%Y-%m-%d")
    end_date = (start_date + dt.timedelta(days=32)).replace(day=1)
    params = {
        "filter": f"from_publication_date:{start_date.date()},to_publication_date:{end_date.date()}",
        "per-page": 50,
        "sort": "publication_date:asc",
    }
    try:
        resp = requests.get(settings.openalex_base_url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for work in data.get("results", []):
            results.append(
                {
                    "title": work.get("title", ""),
                    "abstract": work.get("abstract_inverted_index", {}),
                    "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", []) if a.get("author")],
                    "published": work.get("publication_date", start_date.date().isoformat()),
                    "url": work.get("id"),
                    "doi": work.get("doi"),
                    "categories": work.get("concepts", []),
                    "raw": work,
                }
            )
        return results
    except Exception as exc:  # pragma: no cover
        logger.warning("OpenAlex fetch failed, returning fallback", exc_info=exc)
        sample = {
            "title": "Sample OpenAlex Paper",
            "abstract": "Offline sample abstract for OpenAlex.",
            "authors": ["OpenAlex Author"],
            "published": start_date.date().isoformat(),
            "url": "https://openalex.org/W000000",
            "doi": "10.0000/sample",
            "categories": ["Artificial intelligence"],
            "raw": {},
        }
        return [sample]
