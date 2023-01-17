import json
import random

from behave import *
from behave.runner import Context
from requests import Response

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


def construct_random_path() -> str:
    full_path = ""
    # noinspection SpellCheckingInspection
    valid_symbols = "abcdefghijklmnopqrstuvwxyz-"
    while True:
        partial_path = []
        for _ in range(random.choice(range(3, 12))):
            partial_path.append(random.choice(valid_symbols))
        full_path += f"/{''.join(partial_path)}"
        if random.random() > 0.3:
            break
    return full_path


class ErrorTestCase:

    def __init__(self, request: str, response: Response):
        self.request = request
        self.response = response


@when("a non-documented api endpoint is fetched")
def step_impl(context):
    context.test_cases = []
    for _ in range(context.repetitions):
        random_fetch = construct_random_path()
        print(f"GET {random_fetch}")
        context.test_cases.append(ErrorTestCase(random_fetch, context.client.get(random_fetch)))


@then("404 is received for every fetch attempt")
def step_impl(context):
    for test_case in context.test_cases:
        expected_model = {"detail": "Not Found"}
        actual_model = test_case.response.json()
        assert test_case.response.status_code == 404, \
            f"Expected response to have status code 404 but had, " + \
            test_case.response.status_code
        assert_valid_model(expected_model, actual_model)
