import json
import random

from behave import *
from behave.runner import Context


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

def parse_value(value: str):
    if value.isnumeric():
        return int(value)
    return value


def parse_to_dict(table):
    return {name: parse_value(value) for name, value in table}


@then("the following data is received")
def step_impl(context: Context):
    expected_model = parse_to_dict(context.table)
    actual_model = context.response.json()
    assert_valid_model(actual_model, expected_model)


def assert_valid_model(actual_model, expected_model):
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
    assert_valid_model(actual_model, expected_model)
