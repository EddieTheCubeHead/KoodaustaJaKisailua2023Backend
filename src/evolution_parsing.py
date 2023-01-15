from typing import Any

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
        "shed": "Have a free slot in your party and at least one poke ball while evolving Nincada into Ninjask",
        "agile-style-move": "Use agile style {} 20 times",
        "strong-style-move": "Use strong style {} 20 times",
        "recoil-damage": "Lose at least 294 hp from recoil without fainting"
    }
    formatted_triggers = ("agile-style-move", "strong-style-move")
    if json['trigger']['name'] in triggers:
        trigger_string = triggers[json['trigger']['name']]
    else:
        trigger_string = _get_english_translation_for_entry(json['trigger']['url'])
    return f"{trigger_string}{_parse_evolution_details(json)}" if json["trigger"]["name"] not in formatted_triggers \
        else trigger_string.format(_get_english_translation_for_entry(json["known_move"]["url"]))


def _parse_evolution_details(json: dict):
    base_condition = ""
    if "item" in json and json["item"]:
        name = _get_english_translation_for_entry(json["item"]["url"])
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
        "turn_upside_down": _parse_upside_down
    }
    detail_strings = [detail_parsers[detail](json[detail]) for detail in detail_parsers if json[detail] is not None]
    detail_strings = _prune_list(detail_strings)
    if detail_strings:
        return f"{base_condition} while {_create_plural(*detail_strings)}"
    return f"{base_condition}"


def _prune_list(to_prune: list[Any]) -> list[str]:
    return [item for item in to_prune if type(item) is str]


def _create_plural(*singulars: str):
    if len(singulars) == 1:
        return singulars[0]
    return f"{', '.join(singulars[:-1])} and {singulars[-1]}"


def _parse_gender_details(details: int) -> str:
    gender_mapping = {1: "female", 2: "male"}
    return f"being {gender_mapping[details]}"


def _parse_held_item(details: dict) -> str:
    return f"is holding the item {_get_english_translation_for_entry(details['url'])}"


def _parse_known_move(details: dict) -> str:
    return f"knowing the move {_get_english_translation_for_entry(details['url'])}"


def _parse_known_move_type(details: dict) -> str:
    return f"knowing a {_get_english_translation_for_entry(details['url'])} type move"


def _parse_location(details: dict) -> str:
    return f"in {_get_english_translation_for_entry(details['url'])}"


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


def _parse_party_species(details: dict) -> str:
    return f"having {_get_english_translation_for_entry(details['url'])} in the party"


def _parse_party_type(details: dict) -> str:
    return f"having a {_get_english_translation_for_entry(details['url'])} type pokemon in the party"


def _parse_relative_physical_stats(details: int) -> str:
    relations = {
        -1: "smaller than",
        0: "equal to",
        1: "greater than"
    }
    return f"attack is {relations[details]} defence"


def _parse_time_of_day(details: str | None) -> str:
    return f"it is {details}" if details else None


def _parse_trade_species(details: dict) -> str:
    return f"the other traded pokemon is {_get_english_translation_for_entry(details['url'])}"


def _parse_upside_down(condition: bool) -> str:
    return "the console is held upside down" if condition else None


def _get_english_translation_for_entry(url: str) -> str:
    response = requests.get(url).json()
    names = response["names"]
    return next((name["name"] for name in names if name["language"]["name"] == "en"), response["name"])
