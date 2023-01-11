import requests
from behave import *
from behave.runner import Context


@then("received type matrix that contains the following types and only the following types")
def step_impl(context: Context):
    expected_types = context.text.replace("\r", "").replace("\n", " ").split(", ")
    response = context.response.json()
    actual_types_columns = response[0]
    actual_types_rows = [row[0] for row in response[1:]]
    assert actual_types_columns == actual_types_rows,\
        f"Expected both axes of the type matrix to contain same types in the same order, but columns had " \
        f"types {actual_types_columns} while rows had types {actual_types_rows}."
    actual_types = actual_types_columns
    assert len(expected_types) == len(actual_types_columns),\
        f"Expected to receive {len(expected_types)} types in the matrix but received {len(actual_types)}." \
        f"(Expected types were {expected_types} but received {actual_types}"
    for expected_type in expected_types:
        assert expected_type in actual_types, f"Expected to find the type {expected_type} in {actual_types}"


@then("received type matrix where every matchup row has {amount} multipliers")
def step_impl(context: Context, amount: str):
    amount = int(amount)
    rows_to_validate = context.response.json()[1:]
    for type_name, multipliers in ((row[0], row[1:]) for row in rows_to_validate):
        assert all([type(item) in (float, int) for item in multipliers]),\
            "Expected all multipliers to be integers or floats"
        assert len(multipliers) == amount, f"Expected to receive {amount} multipliers for type {type_name}, but " \
                                           f"received {len(multipliers)} ({multipliers})"


def parse_actual_multipliers(actual_multipliers_raw: dict, type_ordering: list[str]) -> list[float | int]:
    parsed_multipliers = []
    for type_name in type_ordering:
        if type_name in [type_data["name"] for type_data in actual_multipliers_raw["double_damage_to"]]:
            parsed_multipliers.append(2)
        elif type_name in [type_data["name"] for type_data in actual_multipliers_raw["half_damage_to"]]:
            parsed_multipliers.append(0.5)
        elif type_name in [type_data["name"] for type_data in actual_multipliers_raw["no_damage_to"]]:
            parsed_multipliers.append(0)
        else:
            parsed_multipliers.append(1)
    return parsed_multipliers


def assert_correct_multipliers(type_name: str, actual_multipliers: list[float | int], type_ordering: list[str]):
    expected_multipliers_raw = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}").json()["damage_relations"]
    expected_multipliers = parse_actual_multipliers(expected_multipliers_raw, type_ordering)
    assert actual_multipliers == expected_multipliers,\
        f"Expected to receive multipliers {expected_multipliers}, but received {actual_multipliers}"


@then("every row of the received type matrix should have the correct multipliers for the type it represents")
def step_impl(context: Context):
    response = context.response.json()
    type_ordering = response[0]
    actual_multipliers = {row[0]: row[1:] for row in response[1:]}
    for type_name, type_multipliers in actual_multipliers.items():
        assert_correct_multipliers(type_name, type_multipliers, type_ordering)
