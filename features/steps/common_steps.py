import json

from behave import *
from behave.runner import Context

from features.steps.step_helpers import get, post, parse_to_dict, assert_valid_model


@when("getting root")
def step_impl(context: Context):
    get(context, "/")


@when("getting {route}")
def step_impl(context: Context, route: str):
    get(context, route)


@given("data")
def given_data(context: Context):
    context.data = json.loads(context.text) 


@when("posting {route}")
def step_impl(context: Context, route: str):
    post(context, route)


@then("the following data is received")
def step_impl(context: Context):
    expected_model = parse_to_dict(context.table)
    actual_model = context.response.json()
    assert_valid_model(expected_model, actual_model)


@then("404 is received")
def step_impl(context: Context):
    expected_model = {"detail": "Not Found"}
    actual_model = context.response.json()
    assert context.response.status_code == 404, \
        f"Expected response to have status code 404 but had, " + \
        context.response.status_code
    assert_valid_model(expected_model, actual_model)