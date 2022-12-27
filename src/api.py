import requests
from src.experiences import add_experience, get_experience

from src.deserialization import deserialize_growth_rate, deserialize_pokemon, deserialize_pokemon_species
from src.models import GrowthRate, Pokemon, PokemonSpecies, WinBattle, WinBattleParams, GrowthRateExperienceLevel


def get_pokemon(name: str) -> Pokemon:
    request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    return deserialize_pokemon(request.json())


def get_pokemon_species(name: str) -> PokemonSpecies:
    request = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}")
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
        exp_gain = int((fainted_pokemon.base_experience * params.fainted.level) / 5 *
                       (((2 * params.fainted.level + 10) / (params.fainted.level + cur_level + 10)) ** 2.5 + 1))
        
        add_experience(params.winner_name, exp_gain)

        new_experience = get_experience(params.winner_name)
        new_level = find_level_by_exp(params.winner_name, new_experience)

        return WinBattle(level=new_level.level, experience=new_experience)
