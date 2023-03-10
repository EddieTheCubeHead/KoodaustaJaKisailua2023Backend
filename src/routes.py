from src.application import application
from src.api import get_pokemon, get_pokemon_list, get_type, win_battle, get_type_matrix
from src.models import Pokemon, WinBattle, WinBattleParams, TypeMatrix, Type, PokemonList

app = application


@app.get("/")
async def root() -> Pokemon:
    return get_pokemon("bulbasaur")


@app.get("/pokemon/{name}")
async def fetch_pokemon(name: str) -> Pokemon:
    return get_pokemon(name)


@app.get("/pokemon")
async def fetch_pokemon_list(start: int = 0, end: int = 10) -> PokemonList:
    return get_pokemon_list(start, end)


@app.post("/win-battle")
async def route_win_battle(params: WinBattleParams) -> WinBattle:
    return win_battle(params)


@app.get("/type/{name}")
async def fetch_type(name: str) -> Type:
    return get_type(name)


@app.get("/types")
async def fetch_type_matrix() -> TypeMatrix:
    return get_type_matrix()
