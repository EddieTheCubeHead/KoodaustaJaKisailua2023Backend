from functools import lru_cache

from fastapi import HTTPException
import requests


@lru_cache
def get(url: str):
    request = requests.get(url)
    if request.status_code != 200:
        raise HTTPException(request.status_code)
    return request
