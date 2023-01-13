import random

import requests
from behave import *
from behave.model import Table
from behave.runner import Context

from features.steps.step_helpers import get, assert_valid_model


@when("fetching a random base pokemon from /pokemon/name")
def step_impl(context: Context):
    context.fetched_name, context.fetched_number = random.choice(context.all_pokemon)
    get(context, f"/pokemon/{context.fetched_name}")


@then("pokemon name and artwork link returned")
def step_impl(context: Context):
    artwork_link = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/" \
                   f"{context.fetched_number}.png"
    expected_model = {"name": context.fetched_name,
                      "artwork_link": artwork_link}
    actual_model = context.response.json()
    assert_valid_model(expected_model, actual_model)


@then("pokemon types and abilities returned")
def step_impl(context: Context):
    pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{context.fetched_name}").json()
    expected_model = {"types": [typing["type"]["name"] for typing in pokemon_data["types"]],
                      "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]]}
    actual_model = context.response.json()
    assert_valid_model(expected_model, actual_model)


def parse_stats(table: Table):
    return {
        "hp": int(table[0][1]),
        "attack": int(table[1][1]),
        "defense": int(table[2][1]),
        "special_attack": int(table[3][1]),
        "special_defense": int(table[4][1]),
        "speed": int(table[5][1])
    }


@then("the following stats are received")
def step_impl(context: Context):
    expected_stats = parse_stats(context.table)
    assert_valid_model(expected_stats, context.response.json()["stats"])


@then("pokemon stats returned")
def step_impl(context):
    pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{context.fetched_name}").json()
    stats = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
    expected_model = {name: value["base_stat"] for name, value in zip(stats, pokemon_data["stats"])}
    actual_model = context.response.json()["stats"]
    assert_valid_model(expected_model, actual_model)
