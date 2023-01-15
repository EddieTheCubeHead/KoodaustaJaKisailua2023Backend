import requests

from application import API_URL
from deserialization import deserialize_pokemon, deserialize_evolution_chain
from models import Pokemon, EvolutionChain
from pokeapi_client import get


def get_species_pokedex_number(species_url: str) -> int | None:
    species_data = get(species_url)
    numbers = species_data.json()["pokedex_numbers"]
    return None if not numbers else next(number["entry_number"] for number in numbers
                                         if number["pokedex"]["name"] == "national")


def get_pokemon_data(name: str) -> Pokemon:
    variety_name = try_get_default_variety(name)
    form_request = get(f"{API_URL}/pokemon/{variety_name}")
    pokemon = deserialize_pokemon(form_request.json())
    pokemon.evolution_chain = get_evolution_chain(form_request.json()["species"]["url"])
    pokemon.pokedex_number = get_species_pokedex_number(form_request.json()["species"]["url"])
    return pokemon


def try_get_default_variety(species_name: str) -> str:
    request = requests.get(f"{API_URL}/pokemon-species/{species_name}")
    if request.status_code == 200:
        return next(variety["pokemon"]["name"] for variety in request.json()["varieties"] if variety["is_default"])
    return species_name


def get_evolution_chain(species_uri: str) -> EvolutionChain | None:
    family_request = get(species_uri)
    response = family_request.json()
    if "evolution_chain" in response and response["evolution_chain"] and "url" in response["evolution_chain"]:
        species_request = get(family_request.json()["evolution_chain"]["url"])
        return deserialize_evolution_chain(species_request.json())
