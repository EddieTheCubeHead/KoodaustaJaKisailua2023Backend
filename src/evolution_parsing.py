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
    if "item" in json and json["item"]:
        names = requests.get(json["item"]["url"]).json()["names"]
        name = next(name["name"] for name in names if name["language"]["name"] == "en")
        return f" {name}"
    details = {
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
    detail_strings = [details[detail](json[detail]) for detail in details if json[detail]]
    if detail_strings:
        return f" while {_create_plural(*detail_strings)}"
    return ""


def _create_plural(*singulars: str):
    if len(singulars) == 1:
        return singulars[0]
    return f"{', '.join(singulars[:-1])} and {singulars[-1]}"


def _parse_gender_details(details: str) -> str:
    return f"is {details}"


def _parse_held_item(details: str) -> str:
    return f"is holding {details}"


def _parse_known_move(details: str) -> str:
    return f"knows the move {details}"


def _parse_known_move_type(details: str) -> str:
    return f"knows a move of type {details}"  # TODO double check


def _parse_location(details: str) -> str:
    return f"in location {details}"


def _parse_affection(details: str) -> str:
    return f"affection is over {details}"


def _parse_beauty(details: str) -> str:
    return f"beauty is over {details}"


def _parse_happiness(details: str) -> str:
    return f"happiness is over {details}"


def _parse_level(details: str) -> str:
    return f"level is over {details}"


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
