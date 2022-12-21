import requests

from src.deserialization import deserialize_pokemon
from src.models import Pokemon


def get_pokemon(name: str) -> Pokemon:
    request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    return deserialize_pokemon(request.json())
