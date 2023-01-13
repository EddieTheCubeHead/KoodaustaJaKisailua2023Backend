import json
from behave import *
from behave.runner import Context

from features.steps.step_helpers import assert_valid_model_list


@then("list {json_file} is received")
def json_is_received(context: Context, json_file: str):
    file = open(json_file)
    expected_list = json.load(file)
    file.close()
    actual_list = context.response.json()
    assert_valid_model_list(expected_list, actual_list)


@then("the length of the list is {length}")
def length_of_list(context: Context, length: int):
    length = int(length)
    actual_list = context.response.json()
    assert len(actual_list) == length, \
        f"Expected the length of the list to equal {length} " \
        f"but was {len(actual_list)}"