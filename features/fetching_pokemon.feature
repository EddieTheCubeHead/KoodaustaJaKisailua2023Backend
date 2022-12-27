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

  Scenario: Getting ditto from /pokemon route
    When getting /pokemon/ditto
    Then the following data is received
      | data field     | field value |
      | name           | ditto       |
      | pokedex_number | 132         |
      | artwork_link   | https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png |
