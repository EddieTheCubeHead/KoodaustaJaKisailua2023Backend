import json
import random
import re

import requests
from behave import *
from behave.runner import Context

from src.models import EvolutionChain


@when("getting root")
def step_impl(context: Context):
    get(context, "/")


@when("getting {route}")
def step_impl(context: Context, route: str):
    get(context, route)

@given("data")
def given_data(context):
    context.data = json.loads(context.text) 

@when("posting {route}")
def step_impl(context: Context, route: str):
    post(context, route)

def get(context: Context, route: str):
    context.response = context.client.get(route)

def post(context: Context, route: str):
    context.response = context.client.post(route, data=json.dumps(context.data))

def parse_string_list(value: str):
    return [str(item) for item in value[1:-1].split(", ")] if value[1:-1] else []


def parse_value(value: str):
    if value.isnumeric():
        return int(value)
    if re.match(r"\[(?:[\w -]+, )*([\w -]+)]", value):  # list of words: [word, word] or [word]
        return parse_string_list(value)
    return value


def parse_to_dict(table):
    return {name: parse_value(value) for name, value in table}


@then("the following data is received")
def step_impl(context: Context):
    expected_model = parse_to_dict(context.table)
    actual_model = context.response.json()
    assert_valid_model(expected_model, actual_model)


def assert_valid_model(expected_model, actual_model):
    for expected_key, expected_value in expected_model.items():
        assert expected_key in actual_model, \
            f"Expected to find the field '{expected_key}' in the model {actual_model}"
        assert actual_model[expected_key] == expected_value, \
            f"Expected the field '{expected_key}' to equal '{expected_value}' in the model {actual_model}, but was " \
            f"'{actual_model[expected_key]}'"


@when("fetching a random pokemon from /pokemon/name")
def step_impl(context: Context):
    context.fetched_name, context.fetched_number = random.choice(context.all_pokemon)
    get(context, f"/pokemon/{context.fetched_name}")


@then("pokemon name, pokedex number and artwork link returned")
def step_impl(context: Context):
    artwork_link = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/" \
                   f"{context.fetched_number}.png"
    expected_model = {"name": context.fetched_name,
                      "pokedex_number": context.fetched_number,
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


def parse_evolution_from_text(text: str):
    models: dict[str, EvolutionChain] = {}
    rows = text.split("\n")[::-1]
    last_parsed = ""
    for name, pokedex_number, evolution_condition, evolves_to_raw in [row.split(", ") for row in rows]:
        last_parsed = name
        evolves_to = [models[evolution] for evolution in parse_string_list(evolves_to_raw)]
        sprite_link = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokedex_number}.png"
        model = EvolutionChain(name, int(pokedex_number), sprite_link, evolution_condition, evolves_to)
        models[name] = model
    return models[last_parsed]


def all_branches_traversed(branch: dict, parsed: dict[str: EvolutionChain]) -> bool:
    return all([sub_branch["name"] in parsed for sub_branch in branch])


def find_deepest(dictionary: dict, parsed: dict[str: EvolutionChain]) -> dict:
    current_branch = dictionary
    while not all_branches_traversed(current_branch["evolves_to"], parsed):
        current_branch = next(branch for branch in current_branch["evolves_to"] if branch["name"] not in parsed)
    return current_branch


def parse_evolution_from_dict(dictionary: dict) -> EvolutionChain:
    parsed: dict[str, EvolutionChain] = {}
    while dictionary["name"] not in parsed:
        deepest_model = find_deepest(dictionary, parsed)
        parsed_model = EvolutionChain(deepest_model["name"], int(deepest_model["pokedex_number"]),
                                      deepest_model["sprite_link"], deepest_model["evolution_condition"],
                                      [parsed[model["name"]] for model in deepest_model["evolves_to"]])
        parsed[deepest_model["name"]] = parsed_model
    return parsed[dictionary["name"]]


def sanitize(text):
    return text.replace("\r", "")


@then("the following evolution chain is received")
def step_impl(context: Context):
    expected_evolution_model = parse_evolution_from_text(sanitize(context.text))
    actual_evolution_model = parse_evolution_from_dict(context.response.json()["evolution_chain"])
    assert expected_evolution_model == actual_evolution_model,\
        f"expected {expected_evolution_model} to equal {actual_evolution_model}"
