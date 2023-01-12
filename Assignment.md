# Koodausta ja Kisailua 2023

---

## Coding assignment: PokéHub

The goal of this coding assignment to write a data fetcher and parser backend server to provide data to a 
ready-made frontend. The backend fetches data from the PokéAPI API. PokéAPI documentation is available at 
https://pokeapi.co/.

The server will be built using FastAPI library. Setup code and an example for providing a route through the library 
are provided in app.py file so contestants can focus on implementing the data fetching

The assignment is scored based on successful tests in the test set. Once you have cloned the repository and 
installed the dependencies based on README.md you can run the tests by running `behave` in the root directory.

The features that will be scored are divided into categories and most of these categories are further divided into 
different difficulty levels. These categories and difficulties are the following:

 - [Pokémon fetching](#pokémon-fetching)
   - [Basic](#pokebasic)
   - [Intermediate](#pokemedium)
   - [Challenging](#pokehard)
 - [Pokémon list fetching](#pokémon-list-fetching)
 - [Type fetching](#type-fetching)
   - [Basic](#typebasic)
   - [Challenging](#typehard)
 - [Exp gain and level calculation on winning battle](#exp-gain-and-level-calculation-on-battle-wins)

Please also read through the [Rules and clarifications](#rules-and-clarifications) section.

---

## Pokémon fetching

The server should be able to fetch pokémon data by pokémon name from PokéAPI. An example of this functionality is 
given in the app.py file. The file contains code that fetches basic data for bulbasaur when calling root.

---

### <a id="pokebasic" /> Basic features

The basic requirements of fetching a pokémon's data include providing the following data when the server is queried 
from the route `GET /pokemon/{name}`:

 - **Pokémon name**
   - Returned as a string in a field named `name`
 - **Pokémon pokédex number**
   - Returned as an int in a field named `pokedex_number`
 - **Pokémon official sprite link**
   - Returned as a string in a field named `artwork_link`

The Pokémon model returned from the route should look like this after this set of features is implemented:
```
{
    "name": "name",
    "pokedex_number": 0,
    "artwork_link": "www.artwork.link"
}
```
See the root route bulbasaur fetch for example if needed.

This set of features is worth 5 points.

---

### <a id="pokemedium" /> Intermediate features

The intermediate requirements of fetching a pokémon's data include providing the following data when the server is 
queried from the route `GET /pokemon/{name}`:
 - **Pokémon type names**
   - Returned as a list of strings in a field named `types`
 - **Pokémon ability names**
   - Returned as a list of strings in a field named `abilities`
 - **Pokémon stats**
   - Returned as a dictionary in a field named `stats`

The pokémon model returned from the route should look like this after the basic features and this set of features are
implemented:
```
{
    "name": "name",
    "pokedex_number": 0,
    "artwork_link": "www.artwork.link",
    "types": ["type1"],
    "abilities": ["ability1"],
    "stats": {
        "hp": 0
        "attack": 0
        "defense": 0
        "special_attack": 0
        "special_defense": 0
        "speed": 0
    }
}
```
Do note that implementing basic level features is not required to implement intermediate level features.

This set of features is worth 4 points.

---

### <a id="pokehard" /> Challenging features

The challenging requirement of fetching a pokémon's data is providing the pokémon's evolution chain data in a field 
named `evolution_chain`. The evolution chain should be a tree-like model, with each node consisting of the following
fields:

 - `name`: Contains the name of the pokémon whose evolution data this node contains
 - `pokedex_number`: Contains the pokédex number of the pokémon whose evolution data this node contains
 - `sprite_link`: Contains the default sprite link of the pokémon whose evolution data this node contains
 - `evolution_condition`: Contains the condition to evolving the previous evolution chain member into the pokémon whose 
evolution data this node contains. Exact parsing rules given below.
 - `evolves_to`: A list of evolution data nodes containing all the possible evolutions of the pokémon whose evolution 
data this node contains

The evolution condition string should be parsed from the `evolution_details` field present in PokéAPI 
`/evolution-chain/{id}` endpoint return model. The `evolution_details` of one pokémon consists of a list of 
evolution detail models. Only the first model should be parsed. The model has a list of conditions and a `trigger` 
field. The trigger field specifies the trigger that causes the evolution, if all the conditions are met. The trigger 
condition should be the first part of the evolution condition string mapped according to the following list:

 - `level-up` should produce the text `Level up`, with possible condition explanation
 - `trade` should produce the text `Trade`, with possible condition explanation
 - `use-item` should produce the text `Use the item {item_name}`, where `item_name` is the english localization name 
   of the item, available through the `names` field in the PokéAPI `/item/{id}` endpoint. The item that should be 
   used can be found in the `item` field of the evolution detail model. No further condition explanation is necessary.
 - `shed` should produce the text `Have a free slot in your party and at least one poke ball while evolving Nincada 
   into Ninjask`. No further condition explanation is necessary.
 - Other triggers should fetch the trigger explanation localized in english from the PokéAPI `evolution_trigger/{id}` 
   endpoint. No further condition explanation is necessary.

The condition explanation should be constructed from the detail fields. If a condition exists, it should be preceded by
`while` and if a condition exists of more parts (1, 2, 3), the last and second-to-last parts should be separated by an
`and` while the rest should be separated by commas. Therefore, trigger `level-up` with conditions `1, 2, 3` should be
returned as `Level up while 1, 2 and 3`. The formatting for all the different conditions are as follows:

 - `gender`: `being {gender}`
 - `held_item`: `is holding the item {item_name}`, where `item_name` is the english localization of the item name
 - `known_move`: `knowing the move {move_name}`, where `move_name` is the english localization of the move name
 - `known_move_type`: `knowing a {type_name} type move`, where `type_name` is the english localization of the type name
 - `location`: `in {location_name}`, where `location_name` is the english localization of the location name
 - `min_{value}`: `{value} is at least {amount}`, for example `level is at least 1`
 - `needs_overworld_rain`: `it is raining`
 - `party_species`: `having {pokemon_name} in the party`, where `pokemon_name` is the english localization of 
   the party pokémon name
 - `party_type`: `having a {type_name} type pokemon in the party`, where `type_name` is the english localization of 
   the type name
 - `relative_physical_stats`: `attack is {comparison} defence`, where `comparison` is `greater than`, `less than` or 
   `equal to`
 - `time_of_day`: `it is {time_of_day}`, where `time_of_day` is the string provided in the field
 - `trade_species`: `the other traded pokemon is {pokemon_name}`, where `pokemon_name` is the english localization of 
   the traded pokémon name,
 - `turn_upside_down`: `the console is held upside down`

## Pokémon list fetching

## Type fetching

### <a id="typebasic" /> Basic features

### <a id="typehard" /> Challenging features

## Exp gain and level calculation on battle wins

## Rules and clarifications