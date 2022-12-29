import requests

from src.models import EvolutionChain


def deserialize_chain_member(json: dict) -> EvolutionChain:
    pokedex_number = int(json["species"]["url"].split("/")[-2])
    sprite_link = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokedex_number}.png"
    evolution_condition = _parse_evolution_condition(json["evolution_details"])
    evolves_to = [deserialize_chain_member(sub_model) for sub_model in json["evolves_to"]]
    return EvolutionChain(json["species"]["name"], pokedex_number, sprite_link, evolution_condition, evolves_to)


def _parse_evolution_condition(json: dict) -> str:
    if not json:
        return ""
    json = json[0]
    triggers = {
        "level-up": "Level up",
        "trade": "Trade",
        "use-item": "Use the item",
        "shed": "Have a free slot in your party while evolving Nincada",
        "spin": "Spin your trainer",
        "tower-of-darkness": "Train in the tower of darkness",
        "tower-of-waters": "Train in the tower of waters",
        "three-critical-hits": "Land three critical hits in one battle",
        "take-damage": "Go to a specified location after taking damage",
        "other": "Unavailable"
    }
    return f"{triggers[json['trigger']['name']]}{_parse_evolution_details(json)}"


def _parse_evolution_details(json: dict):
    base_condition = ""
    if "item" in json and json["item"]:
        name = get_item_name(json["item"]["url"])
        base_condition = f" {name}"
    detail_parsers = {
        "gender": _parse_gender_details,
        "held_item": _parse_held_item,
        "known_move": _parse_known_move,
        "known_move_type": _parse_known_move_type,
        "location": _parse_location,
        "min_affection": _parse_affection,
        "min_beauty": _parse_beauty,
        "min_happiness": _parse_happiness,
        "min_level": _parse_level,
        "needs_overworld_rain": _parse_rain,
        "party_species": _parse_party_species,
        "party_type": _parse_party_type,
        "relative_physical_stats": _parse_relative_physical_stats,
        "time_of_day": _parse_time_of_day,
        "trade_species": _parse_trade_species,
    }
    detail_strings = [detail_parsers[detail](json[detail]) for detail in detail_parsers if json[detail]]
    if detail_strings:
        return f"{base_condition} while {_create_plural(*detail_strings)}"
    return f"{base_condition}"


def get_item_name(url: str):
    names = requests.get(url).json()["names"]
    name = next(name["name"] for name in names if name["language"]["name"] == "en")
    return name


def _create_plural(*singulars: str):
    if len(singulars) == 1:
        return singulars[0]
    return f"{', '.join(singulars[:-1])} and {singulars[-1]}"


def _parse_gender_details(details: int) -> str:
    gender_mapping = {1: "female", 2: "male"}
    return f"being {gender_mapping[details]}"


def _parse_held_item(details: dict) -> str:
    return f"is holding the item {get_item_name(details['url'])}"


def _parse_known_move(details: str) -> str:
    return f"knowing the move {details}"


def _parse_known_move_type(details: dict) -> str:
    return f"knowing a {details['name']}-type move"


def _parse_location(details: dict) -> str:
    names = requests.get(details["url"]).json()["names"]
    name = next(name["name"] for name in names if name["language"]["name"] == "en")
    return f"in {name}"


def _parse_affection(details: str) -> str:
    return f"affection is at least {details}"


def _parse_beauty(details: str) -> str:
    return f"beauty is at least {details}"


def _parse_happiness(details: str) -> str:
    return f"happiness is at least {details}"


def _parse_level(details: str) -> str:
    return f"level is at least {details}"


def _parse_rain(condition: bool) -> str:
    return "it is raining" if condition else None


def _parse_party_species(details: str) -> str:
    return f"party has pokemon of the {details} species"  # TODO double check


def _parse_party_type(details: str) -> str:
    return f"party has pokemon of the {details} type"  # TODO double check


def _parse_relative_physical_stats(details: str) -> str:
    return f"has physical stats of {details}"  # TODO fix


def _parse_time_of_day(details: str) -> str:
    return f"it is {details}"


def _parse_trade_species(details: str) -> str:
    return f"traded with {details}"


def _parse_upside_down(details: str) -> str:
    return "game held upside down"
