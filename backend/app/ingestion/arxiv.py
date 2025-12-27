import datetime as dt
import logging
import requests
import feedparser
from typing import List, Dict

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def fetch_arxiv_by_month(month: str) -> List[Dict]:
    # month format YYYY-MM
    start_date = dt.datetime.strptime(month + "-01", "%Y-%m-%d")
    end_date = (start_date + dt.timedelta(days=32)).replace(day=1)
    query = f"submittedDate:[{start_date:%Y%m%d}0000 TO {end_date:%Y%m%d}0000]"
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "ascending",
        "max_results": 100,
    }
    try:
        resp = requests.get(settings.arxiv_base_url, params=params, timeout=15)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        entries = []
        for entry in feed.entries:
            entries.append(
                {
                    "title": entry.get("title", "").strip(),
                    "abstract": entry.get("summary", "").strip(),
                    "authors": [a.name for a in entry.get("authors", [])],
                    "published": entry.get("published", start_date.isoformat()),
                    "url": entry.get("link"),
                    "arxiv_id": entry.get("id", "").split("/")[-1],
                    "categories": entry.get("tags", []),
                    "raw": entry,
                }
            )
        return entries
    except Exception as exc:  # pragma: no cover - network failure fallback
        logger.warning("ArXiv fetch failed, returning fallback payload", exc_info=exc)
        sample = {
            "title": "Sample ArXiv Paper",
            "abstract": "Demonstration abstract for offline use.",
            "authors": ["Offline Author"],
            "published": start_date.isoformat(),
            "url": "https://arxiv.org/abs/0000.00000",
            "arxiv_id": "0000.00000",
            "categories": ["cs.AI"],
            "raw": {},
        }
        return [sample]
