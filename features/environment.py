import requests
from behave.runner import Context
from starlette.testclient import TestClient

from src.routes import app


def before_all(context: Context):
    context.client = TestClient(app)
    context.response = None
    all_pokemon_raw = requests.get("https://pokeapi.co/api/v2/pokemon?limit=9999").json()["results"]
    all_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon_raw]
    all_species_raw = requests.get("https://pokeapi.co/api/v2/pokemon-species?limit=9999").json()["results"]
    all_species = [species["name"] for species in all_species_raw]
    basic_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon_raw
                     if pokemon["name"] in all_species]
    form_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon_raw
                    if pokemon["name"] not in all_species]
    context.all_pokemon = all_pokemon
    context.basic_pokemon = basic_pokemon
    context.form_pokemon = form_pokemon
