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
