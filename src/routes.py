from fastapi import FastAPI

from src.api import get_pokemon
from src.models import Pokemon

app = FastAPI()


@app.get("/")
async def root() -> Pokemon:
    return get_pokemon("bulbasaur")


@app.get("/pokemon/{name}")
async def fetch_pokemon(name: str):
    return get_pokemon(name)
