from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from backend.app.api import admin, analytics
from backend.app.core.config import get_settings
from backend.app.core.rate_limit import rate_limiter
from backend.app.utils.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limiter)

app.include_router(admin.router, prefix=settings.api_v1_prefix)
app.include_router(analytics.router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health():
    return {"status": "ok"}


if settings.metrics_enabled:
    Instrumentator().instrument(app).expose(app)
