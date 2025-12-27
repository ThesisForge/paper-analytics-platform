from fastapi import Depends, Header, HTTPException
from backend.app.core.config import get_settings


settings = get_settings()


def get_api_key(x_api_key: str = Header(None)):
    if x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key
