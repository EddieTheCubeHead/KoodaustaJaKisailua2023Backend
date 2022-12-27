experiences: {str, float} = {}


def add_experience(pokemon_name: str, value: int):
    if pokemon_name not in experiences:
        experiences[pokemon_name] = 0
    experiences[pokemon_name] += value


def get_experience(pokemon_name) -> int | None:
    if pokemon_name not in experiences:
        return None
    return experiences[pokemon_name]
