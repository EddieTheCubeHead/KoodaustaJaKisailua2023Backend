import requests
from src.experiences import add_experience, get_experience

from src.deserialization import deserialize_growth_rate, deserialize_pokemon, deserialize_pokemon_species, \
    deserialize_evolution_chain
from src.models import GrowthRate, Pokemon, PokemonSpecies, WinBattle, WinBattleParams, GrowthRateExperienceLevel, \
    EvolutionChain

API_URL = "https://pokeapi.co/api/v2"


def get_evolution_chain(name: str) -> EvolutionChain | None:
    family_request = requests.get(f"{API_URL}/pokemon-species/{name}")
    if family_request.status_code == 200 and "url" in family_request.json()["evolution_chain"]:
        species_request = requests.get(family_request.json()["evolution_chain"]["url"])
        return deserialize_evolution_chain(species_request.json())


def get_pokemon(name: str) -> Pokemon:
    request = requests.get(f"{API_URL}/pokemon/{name}")
    pokemon = deserialize_pokemon(request.json())
    pokemon.evolution_chain = get_evolution_chain(name)
    return pokemon


def get_pokemon_species(name: str) -> PokemonSpecies:
    request = requests.get(f"{API_URL}/pokemon-species/{name}")
    return deserialize_pokemon_species(request.json())


def get_growth_rate_with_pokemon(name: str) -> GrowthRate:
    species = get_pokemon_species(name)
    request = requests.get(species.growth_rate.url)
    return deserialize_growth_rate(request.json())


def find_level_by_exp(name: str, exp: int) -> GrowthRateExperienceLevel:
    growth_rate = get_growth_rate_with_pokemon(name)
    for level in growth_rate.levels:
        if level.experience >= exp:
            return level


def win_battle(params: WinBattleParams) -> WinBattle:
    winner_pokemon = get_pokemon(params.winner_name)
    fainted_pokemon = get_pokemon(params.fainted.name)
    if fainted_pokemon and fainted_pokemon.base_experience:
        cur_exp = get_experience(params.winner_name)
        cur_exp = cur_exp if cur_exp is not None else winner_pokemon.base_experience
        cur_level = find_level_by_exp(params.winner_name, cur_exp).level

        # https://bulbapedia.bulbagarden.net/wiki/Experience#Experience_at_each_level:~:text=The%20scaled%20formula%20in%20Generation%20VII,.
        # We only use b, L and L_p variables. Others can be treated as 1.
        exp_gain = (fainted_pokemon.base_experience * params.fainted.level) / 5 * \
                    (((2 * params.fainted.level + 10) / (params.fainted.level + cur_level + 10)) ** 2.5 + 1)
        
        add_experience(params.winner_name, exp_gain)

        new_experience = get_experience(params.winner_name)
        new_level = find_level_by_exp(params.winner_name, new_experience)

        return WinBattle(level=new_level.level, experience=round(new_experience))
