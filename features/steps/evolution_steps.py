from behave import *
from behave.runner import Context

from src.models import EvolutionChain
from features.steps.step_helpers import parse_string_list


def parse_evolution_from_text(text: str):
    models: dict[str, EvolutionChain] = {}
    rows = text.split("\n")[::-1]
    last_parsed = ""
    for name, pokedex_number, evolution_condition, evolves_to_raw in [row.split(", ", 3) for row in rows]:
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


def assert_valid_evolution(expected_evolution: EvolutionChain, actual_evolution: EvolutionChain):

    assert expected_evolution.name == actual_evolution.name, \
        f"Expected evolution model name to be {expected_evolution.name}, but was {actual_evolution.name}"

    assert expected_evolution.pokedex_number == actual_evolution.pokedex_number, \
        f"Expected {actual_evolution.name} evolution model pokedex number to be " \
        f"{expected_evolution.pokedex_number}, but was {actual_evolution.pokedex_number}"

    assert expected_evolution.sprite_link == actual_evolution.sprite_link, \
        f"Expected {actual_evolution.name} evolution model sprite link to be " \
        f"{expected_evolution.sprite_link}, but was {actual_evolution.sprite_link}"

    assert expected_evolution.evolution_condition == actual_evolution.evolution_condition, \
        f"Expected {actual_evolution.name} evolution model evolution condition to be " \
        f"{expected_evolution.evolution_condition}, but was {actual_evolution.evolution_condition}"

    for expected_evolves_to in expected_evolution.evolves_to:
        actual_evolves_to \
            = next((model for model in actual_evolution.evolves_to if model.name == expected_evolves_to.name), None)
        assert actual_evolves_to is not None, \
            f"Expected to find evolution named {expected_evolves_to.name} in evolutions for evolution model named " \
            f"{actual_evolution.name}, but only found {[model.name for model in actual_evolution.evolves_to]}"
        assert_valid_evolution(expected_evolves_to, actual_evolves_to)


def sanitize(text):
    return text.replace("\r", "")


@then("the following evolution chain is received")
def step_impl(context: Context):
    expected_evolution_model = parse_evolution_from_text(sanitize(context.text))
    actual_evolution_model = parse_evolution_from_dict(context.response.json()["evolution_chain"])
    assert_valid_evolution(expected_evolution_model, actual_evolution_model)