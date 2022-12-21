from behave import *
from behave.runner import Context


@when("getting root")
def step_impl(context: Context):
    get(context, "/")


@when("getting {route}")
def step_impl(context: Context, route: str):
    get(context, route)


def get(context: Context, route: str):
    context.response = context.client.get(route)


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
    for expected_key, expected_value in expected_model.items():
        assert expected_key in actual_model, \
            f"Expected to find the field '{expected_key}' in the model {actual_model}"
        assert actual_model[expected_key] == expected_value, \
            f"Expected the field '{expected_key}' to equal '{expected_value}' in the model {actual_model}, but was " \
            f"'{actual_model[expected_key]}'"
