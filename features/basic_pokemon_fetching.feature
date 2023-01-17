# Created by MustacheCorp at 21/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}", basic level
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # Root should return the same as calling "/pokemon/bulbasaur"
  # The minimum requirements for the route are providing the name, pokedex number and a link to the official artwork
  # Providing the pokedex number and artwork link is required for pokemon from generations I to VIII with no forms

  Scenario: Getting bulbasaur from root
    When getting root
    Then the following data is received
      | data field     | field value |
      | name           | bulbasaur   |
      | pokedex_number | 1           |
      | artwork_link   | https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png |

  Scenario Outline: Getting a pokemon from the /pokemon route with base information
    When getting /pokemon/<name>
    Then the following data is received
      | data field     | field value |
      | name           | <name>      |
      | pokedex_number | <id>        |
      | artwork_link   | https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/<id>.png |

    Examples: Blaziken
      | name     | id  |
      | blaziken | 257 |

    Examples: Spiritomb
      | name      | id  |
      | spiritomb | 442 |

    Examples: Ditto
      | name      | id  |
      | ditto     | 132 |

    Examples: Deoxys-Normal
      | name          | id  |
      | deoxys-normal | 386 |

  Scenario: Getting a random pokemon from the /pokemon route with base information
    When fetching a random base pokemon from /pokemon/name
    Then pokemon name and artwork link returned
