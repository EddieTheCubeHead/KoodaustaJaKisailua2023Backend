import requests
from behave.runner import Context
from starlette.testclient import TestClient

from src.routes import app


_DEFAULT_REPETITIONS = 10


def before_all(context: Context):
    context.client = TestClient(app)
    context.response = None
    context.repetitions = int(context.config.userdata.get("repetitions", _DEFAULT_REPETITIONS))
    all_pokemon_raw = requests.get("https://pokeapi.co/api/v2/pokemon?limit=9999").json()["results"]
    all_species_raw = requests.get("https://pokeapi.co/api/v2/pokemon-species?limit=9999").json()["results"]
    all_species = [species["name"] for species in all_species_raw]
    basic_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon_raw[:905]
                     if pokemon["name"] in all_species]
    complex_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon_raw
                       if pokemon["name"] not in (item[0] for item in basic_pokemon)]
    context.basic_pokemon = basic_pokemon
    context.complex_pokemon = complex_pokemon
