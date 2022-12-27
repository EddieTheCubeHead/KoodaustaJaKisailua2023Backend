import requests
from behave.runner import Context
from starlette.testclient import TestClient

from src.routes import app


def before_all(context: Context):
    context.client = TestClient(app)
    context.response = None
    all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=9999").json()["results"]
    context.all_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon]
