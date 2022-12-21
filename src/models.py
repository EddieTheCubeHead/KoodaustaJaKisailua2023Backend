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
    offensive_multipliers: {str: float}
    defensive_multipliers: {str: float}


TypeMatrix = list[list[str|float]]


@dataclass
class ExpGainPokemonData:
    name: str
    level: int


@dataclass
class ExpGainParams:
    attacker: ExpGainPokemonData
    defender: ExpGainPokemonData


@dataclass
class ExpGain:  # route: /exp_gain, params: ExpGainParams
    exp_gained: int
