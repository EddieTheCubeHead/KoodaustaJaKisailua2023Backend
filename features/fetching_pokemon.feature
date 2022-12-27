# Created by MustacheCorp at 21/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # Root should return the same as calling "/pokemon/bulbasaur"
  # The minimum requirements for the route are providing the name, pokedex id and a link to the official artwork

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
      | data field     | field value      |
      | name           | <name>           |
      | pokedex_number | <pokedex number> |
      | artwork_link   | https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/<pokedex number>.png |

    Examples: Blaziken
      | name     | pokedex number |
      | blaziken | 257            |

    Examples: Spiritomb
      | name      | pokedex number |
      | spiritomb | 442            |

    Examples: Ditto
      | name      | pokedex number |
      | ditto     | 132            |

    # Add examples here to fill the point requirements

  # Duplicate this if deemed necessary
  Scenario: Getting a random pokemon from the /pokemon route with base information
    When fetching a random pokemon from /pokemon/name
    Then pokemon name, pokedex number and artwork link returned
      | data field     | field value |
      | name           | ditto       |
      | pokedex_number | 132         |
      | artwork_link   | https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png |

  Scenario: Calculating battle win
    Given data
    """
    {
      "winner_name": "bulbasaur", 
      "fainted": {
        "name": "pikachu", 
        "level": 5
      }
    }
    """
    When posting /win-battle 
    Then the following data is received
      | data field     | field value |
      | level          | 8           |
      | experience     | 239         |

  Scenario: Calculating battle win stores experience and level
    Given data
    """
    {
      "winner_name": "bulbasaur",
      "fainted": {
        "name": "eevee",
        "level": 10
      }
    }
    """
    When posting /win-battle
    Then the following data is received
      | data field     | field value |
      | level          | 10          |
      | experience     | 524         |

  Scenario: Calculating battle win for another pokemon
    Given data
    """
    {
      "winner_name": "grookey",
      "fainted": {
        "name": "abra",
        "level": 8
      }
    }
    """
    When posting /win-battle
    Then the following data is received
      | data field     | field value |
      | level          | 8           |
      | experience     | 250         |

  Scenario: Calculating battle win for another pokemon stores experience and level
    Given data
    """
    {
      "winner_name": "grookey",
      "fainted": {
        "name": "trapinch",
        "level": 13
      }
    }
    """
    When posting /win-battle
    Then the following data is received
      | data field     | field value |
      | level          | 11          |
      | experience     | 620         | 

      
