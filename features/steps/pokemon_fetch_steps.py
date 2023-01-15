import random

import requests
from behave import *
from behave.model import Table
from behave.runner import Context
from requests import Response

from features.steps.step_helpers import get, assert_valid_model


class FetchTestCase:

    def __init__(self, name: str, pokemon_id: int, response: Response):
        self.name = name
        self.pokemon_id = pokemon_id
        self.response = response


@when("fetching a random base pokemon from /pokemon/name")
def step_impl(context: Context):
    context.fetched = []
    for _ in range(context.repetitions):
        fetched_name, fetched_number = random.choice(context.basic_pokemon)
        route = f"/pokemon/{fetched_name}"
        print(f"GET {route}")
        response = context.client.get(route)
        context.fetched.append(FetchTestCase(fetched_name, fetched_number, response))


@then("pokemon name and artwork link returned")
def step_impl(context: Context):
    for test_case in context.fetched:
        artwork_link = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/" \
                       f"official-artwork/{test_case.pokemon_id}.png"
        expected_model = {"name": test_case.name,
                          "artwork_link": artwork_link}
        actual_model = test_case.response.json()
        assert_valid_model(expected_model, actual_model)


@then("pokemon types and abilities returned")
def step_impl(context: Context):
    for test_case in context.fetched:
        pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{test_case.name}").json()
        expected_model = {"types": [typing["type"]["name"] for typing in pokemon_data["types"]],
                          "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]]}
        actual_model = test_case.response.json()
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
    for test_case in context.fetched:
        pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{test_case.name}").json()
        stats = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
        expected_model = {name: value["base_stat"] for name, value in zip(stats, pokemon_data["stats"])}
        actual_model = test_case.response.json()["stats"]
        assert_valid_model(expected_model, actual_model)


@then("models named {expected_names_raw} received")
def step_impl(context: Context, expected_names_raw: str):
    expected_names_raw.replace("and", ",")
    expected_names = expected_names_raw.split(", ")
    actual_names = [model["name"] for model in context.response.json()]
    for expected_name in expected_names:
        assert expected_name in actual_names, f"Expected to find {expected_name} in {actual_names}"
