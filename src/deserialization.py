from models import Pokemon


def deserialize_pokemon(raw_json: dict) -> Pokemon:
    ability_listing = [ability["ability"]["name"] for ability in raw_json["abilities"]]
    type_listing = [typing["type"]["name"] for typing in raw_json["types"]]
    artwork_link = raw_json["sprites"]["other"]["official-artwork"]["front_default"]
    return Pokemon(name=raw_json["name"], abilities=ability_listing, artwork_link=artwork_link,
                   pokedex_number=raw_json["id"], types=type_listing, evolution_chain=None)
