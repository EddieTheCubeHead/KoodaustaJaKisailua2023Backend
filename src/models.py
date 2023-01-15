from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Stats:
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


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
    pokedex_number: int | None
    artwork_link: str | None
    types: list[str]
    abilities: list[str]
    stats: Stats
    evolution_chain: EvolutionChain | None
    base_experience: int


@dataclass
class ListPokemon:
    name: str
    pokedex_number: int
    sprite_link: str
    types: list[str]


PokemonList = list[ListPokemon]  # route: /pokemon?start=0&end=1008


@dataclass
class Type:  # route: /type/{name}
    name: str
    id: int
    offensive_multipliers: dict[str, float]
    defensive_multipliers: dict[str, float]


TypeMatrix = list[list[str | float]]  # route: /types


@dataclass
class WinBattleFaintedPokemonData:
    name: str
    level: int


@dataclass
class WinBattleParams:
    winner_name: str
    fainted: WinBattleFaintedPokemonData


@dataclass
class WinBattle:  # route: /win-battle, params: WinBattleParams
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
