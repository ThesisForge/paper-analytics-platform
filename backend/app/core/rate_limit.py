import time
from fastapi import HTTPException, Request
from starlette.responses import Response
import redis
from backend.app.core.config import get_settings

settings = get_settings()
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


async def rate_limiter(request: Request, call_next):
    identifier = request.client.host if request.client else "anonymous"
    key = f"rate:{identifier}"
    try:
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, settings.rate_limit_window_seconds)
        if current > settings.rate_limit_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except redis.RedisError:
        # fail open on redis issues
        pass

    response = await call_next(request)
    return response
