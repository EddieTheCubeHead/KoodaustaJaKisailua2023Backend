from enum import Enum


class RelationType(Enum):
    OFFENSIVE = 1
    DEFENSIVE = 2


class RelationMultipliers:
    offensive = {
        "no_damage_to": 0,
        "half_damage_to": 0.5,
        "double_damage_to": 2
    }

    defensive = {
        "no_damage_from": 0,
        "half_damage_from": 0.5,
        "double_damage_from": 2
    }


def parse_multipliers(relations_json: dict, relation_type: RelationType) -> dict[str, float]:
    relations = {}

    if relation_type == RelationType.OFFENSIVE:
        relation_multipliers = RelationMultipliers.offensive
    elif relation_type == RelationType.DEFENSIVE:
        relation_multipliers = RelationMultipliers.defensive
    else:
        raise ValueError("type is missing")

    for relation, multiplier in relation_multipliers.items():
        if relation in relations_json:
            relation_data = relations_json[relation]
            for relation_type in relation_data:
                relations[relation_type["name"]] = multiplier

    return relations
