from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EvolutionChain:
    name: str
    pokedex_number: int
    sprite_link: str
    evolution_condition: str
    evolves_to: list[EvolutionChain]


@dataclass
class Pokemon:  # route: /pokemon/{name}
    name: str
    pokedex_number: int
    artwork_link: str
    types: list[str]
    abilities: list[str]
    evolution_chain: EvolutionChain | None
    base_experience: int


@dataclass
class ListPokemon:  # route: /pokemons?start=0&end=1008
    name: str
    pokedex_number: int
    sprite_link: str
    types: list[str]


@dataclass
class Type:  # route: /type/{name}
    name: str
    id: int
    offensive_multipliers: dict[str, float]
    defensive_multipliers: dict[str, float]


TypeMatrix = list[list[str | float]]


@dataclass
class WinBattleFaintedPokemonData:
    name: str
    level: int


@dataclass
class WinBattleParams:
    winner_name: str
    fainted: WinBattleFaintedPokemonData


@dataclass
class WinBattle:
    level: int
    experience: int


@dataclass
class GrowthRateExperienceLevel:
    level: int
    experience: int


@dataclass
class GrowthRate:
    levels: list[GrowthRateExperienceLevel] 


@dataclass
class PokemonSpecies:
    growth_rate: PokemonSpeciesGrowthRate


@dataclass
class PokemonSpeciesGrowthRate:
    name: str
    url: str
