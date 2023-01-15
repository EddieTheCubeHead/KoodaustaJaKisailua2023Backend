import json
import re

from behave.runner import Context


def get(context: Context, route: str):
    context.response = context.client.get(route)


def post(context: Context, route: str):
    context.response = context.client.post(route, data=json.dumps(context.data))


def parse_string_list(value: str):
    return [str(item) for item in value[1:-1].split(", ")] if value[1:-1] else []


def parse_value(value: str):
    if value.isnumeric():
        return int(value)
    if value == "None":
        return None
    if re.match(r"\[(?:[\w -]+, )*([\w -]+)]", value):  # list of words: [word, word] or [word]
        return parse_string_list(value)
    json_matches = re.findall(r"(?<=json\().*(?=\))", value)
    if json_matches and len(json_matches) == 1:
        return json.loads(json_matches[0])
    return value


def parse_to_dict(table):
    return {name: parse_value(value) for name, value in table}


def assert_valid_model(expected_model, actual_model):
    for expected_key, expected_value in expected_model.items():
        assert expected_key in actual_model, \
            f"Expected to find the field '{expected_key}' in the model {actual_model}"
        assert actual_model[expected_key] == expected_value, \
            f"Expected the field '{expected_key}' to equal '{expected_value}' in the model {actual_model}, but was " \
            f"'{actual_model[expected_key]}'"


def assert_valid_model_list(expected_list, actual_list):
    for index, model in enumerate(expected_list):
        assert_valid_model(model, actual_list[index])
