﻿# Koodausta ja Kisailua 2023

---

## Coding assignment: PokéHub

The goal of this coding assignment is to write a data fetcher and parser backend server to provide data to a 
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
 - [Battle level gain](#battle-level-gain)

Please also read through the [Rules and clarifications](#rules-and-clarifications) section.

---

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

The evolution chain model in the pokémon fetch route's return model's `evolution_chain` field should look like this
after this feature is implemented:

```
{
   "name": "name1",
   "pokedex_number": 1,
   "evolution_condition": "Text here",
   "evolves_to": [
      {
         "name": "name2",
         "pokedex_number": 2,
         "evolution_condition": "Text here",
         "evolves_to": [
            {
               "name": "name3",
               "pokedex_number": 3,
               "evolution_condition": "Text here",
               "evolves_to": []
            }
         ]
      },
      {
         "name": "name4",
         "pokedex_number": 4,
         "evolution_condition": "Text here",
         "evolves_to": [
            {
               "name": "name5",
               "pokedex_number": 5,
               "evolution_condition": "Text here",
               "evolves_to": []
            }
         ]
      }
   ]
}
```

This set of features is worth 20 points.

---

----

## Pokémon list fetching

The pokémon list fetching feature is not divided into different difficulty levels. This feature requires the server to
return a listing of simpler data models when queried for the route `GET /pokemon`. The route should have path parameters
`start` and `end`, which specify the pokédex number of the first and last pokémon to include (unlike list splicing, this
should include also the last number). An example call for the route 

The model returned for each pokémon found should have the following data:

- **Pokémon name**
   - Returned as a string in a field named `name`
 - **Pokémon pokédex number**
   - Returned as an int in a field named `pokedex_number`
 - **Pokémon small sprite link**
   - Returned as a string in a field named `sprite_link`
 - **Pokémon types**
   - Returned as a list of strings in a field named `types`

The whole model returned from the route should look like this after this feature is implemented:

```
[
   {
      "name": "name1",
      "pokedex_number": 1,
      "sprite_link": "www.sprite1.link",
      "types": ["type1", "type2"]
   },
   {
      "name": "name2",
      "pokedex_number": 2,
      "sprite_link": "www.sprite2.link",
      "types": ["type3"]
   }
   ...
]
```

---

---

## Type fetching

The server should be able to fetch type data by type name.

---

### <a id="typebasic" /> Basic features

The basic requirements for type data fetching include providing the following data when the server is queried 
from the route `GET /type/{name}`:

 - **Type name**
   - Returned as a string in a field named `name`
 - **Type id**
   - Returned as an int in a field named `id`

The model returned from the route should look like this after the basic level requirements for this feature are
implemented:

```
{
   "name": "name",
   "id": 0
}
```

---

### <a id="typehard" /> Intermediate features

The intermediate requirements for type data fetching include providing the following data when the server is queried
from the route `GET /type/{name}`

 - **Type offensive multipliers**
   - Returned as a dictionary of type name strings, mapped to floats indicating the multiplier amount in a field named
   `offensive_multipliers`
 - **Type defensive multipliers**
   - Returned as a dictionary of type name strings, mapped to floats indicating the multiplier amountin a field named
   `defensive_multipliers`

The model returned from the route should look like this after the basic and intermediate level requirements for this 
feature are implemented:

```
{
   "name": "name",
   "id": 0,
   "offensive_multipliers": {
      "type1": 0,
      "type2": 0.5,
      "type3": 1,
      "type4": 2
   },
   "defensive_multipliers": {
      "type5": 0,
      "type6": 0.5,
      "type7": 1,
      "type8": 2
   }
}
```

---

---

###  Battle level gain

In the battle level gain feature, the server should provide a `POST /win-battle` endpoint that accepts the following
json in the request body:

```
{
    "winner_name": str,
    "fainted": {
        "name": str,
        "level": int
    }
}
```

With these parameters, the server should calculate the winner pokémon's experience gained if they were to make another
pokémon with a given level faint in the newest generation. The equation to make this calculation can be found 
[here](https://bulbapedia.bulbagarden.net/wiki/Experience#Experience_at_each_level:~:text=The%20scaled%20formula%20in%20Generation%20VII).
The only variables you need to account for are b, L and L_p. Others can be treated as 1. It should then return the
results in the following model:

```
{
    "level": int
    "experience": int
}
```

Note that experience should be rounded to the nearest integer.

To get the full points from this feature, the server should also be able to remember every winner's level and experience. 
When the endpoint is called again with `winner_name` that it has seen earlier, it should perform the equation using the 
stored level and experience. This should be done with an in-memory database so that it is reset between runs.

---

---

## Rules and clarifications

 - Generally failing to follow a rule will result in a warning. Two warnings will result in a disqualification.
 Accidentally breaking the rules will not result in a warning if you inform the organizers right away and fix the
 violation.
 - Adding packages to requirements.txt requires approvement from the organizers: adding a package without getting an
 approvement will result in a warning.
 - All server responses should be based on data fetched from PokéAPI by the server.
 - Modifying any files under the `/features folder` is strictly forbidden. However, reading the files is allowed and 
 even encouraged.
 - You are allowed to edit the example code in app.py. However, you need to keep the `app = FastAPI()` declaration 
 present in the file and keep the file in the `src` folder for the tests to work.
 - Asking for help is allowed and encouraged. You can ask for help live, or send a message to the event discord.