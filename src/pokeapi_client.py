from fastapi import HTTPException
import requests


def get(url: str):
    request = requests.get(url)
    if request.status_code != 200:
        raise HTTPException(request.status_code)
    return request
