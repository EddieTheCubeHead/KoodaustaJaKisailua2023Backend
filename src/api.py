import requests

from deserialization import deserialize_pokemon
from models import Pokemon


def get_pokemon(name: str) -> Pokemon:
    request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    return deserialize_pokemon(request.json())
