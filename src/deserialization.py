import requests

from src.evolution_parsing import deserialize_chain_member
from src.models import GrowthRate, GrowthRateExperienceLevel, Pokemon, PokemonSpecies, PokemonSpeciesGrowthRate, \
    EvolutionChain, Stats


def _parse_stats(stat_list: list[dict]) -> Stats:
    return Stats(*[stat_json["base_stat"] for stat_json in stat_list])


def deserialize_pokemon(raw_json: dict) -> Pokemon:
    ability_listing = [ability["ability"]["name"] for ability in raw_json["abilities"]]
    type_listing = [typing["type"]["name"] for typing in raw_json["types"]]
    artwork_link = raw_json["sprites"]["other"]["official-artwork"]["front_default"]
    base_experience = raw_json["base_experience"]
    stats = _parse_stats(raw_json["stats"])
    return Pokemon(name=raw_json["name"], abilities=ability_listing, artwork_link=artwork_link,
                   pokedex_number=raw_json["id"], types=type_listing, stats=stats, evolution_chain=None,
                   base_experience=base_experience)


def deserialize_growth_rate(raw_json: dict) -> GrowthRate:
    levels = [GrowthRateExperienceLevel(
        level=entry["level"],
        experience=entry["experience"]) for entry in raw_json["levels"]]
    return GrowthRate(levels=levels)


def deserialize_pokemon_species(raw_json: dict) -> PokemonSpecies:
    growth_rate = PokemonSpeciesGrowthRate(
        name=raw_json["growth_rate"]["name"],
        url=raw_json["growth_rate"]["url"]
    )
    return PokemonSpecies(growth_rate=growth_rate)


def deserialize_evolution_chain(raw_json: dict) -> EvolutionChain:
    return deserialize_chain_member(raw_json["chain"])
