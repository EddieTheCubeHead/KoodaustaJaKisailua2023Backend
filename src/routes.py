from src.application import application
from src.api import get_pokemon, get_type, win_battle
from src.models import Pokemon, WinBattle, WinBattleParams


app = application


@app.get("/")
async def root() -> Pokemon:
    return get_pokemon("bulbasaur")


@app.get("/pokemon/{name}")
async def fetch_pokemon(name: str):
    return get_pokemon(name)


@app.post("/win-battle")
async def route_win_battle(params: WinBattleParams) -> WinBattle:
    return win_battle(params)


@app.get("/type/{name}")
async def fetch_type(name: str):
    return get_type(name)
