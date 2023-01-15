# Created by MustacheCorp at 15/01/2023
Feature: Fetching pokemon data based on pokemon species
  # Challenging modification to pokemon data fetching and pokemon list fetching:
  #  - pokedex number should come from species data national dex number and is nullable (Get IX pokemon have no national
  #    dex number
  #  - pokemon fetching should support both form names and species names. Species name should get default variety data
  #  - pokemon list fetching should return the list based on species listed in PokeAPI. The list should use default
  #    variety data

  Scenario Outline: Getting a pokemon from the /pokemon route, species cases
    When getting /pokemon/<name>
    Then the following data is received
      | data field     | field value      |
      | name           | <form_name>      |
      | pokedex_number | <pokedex_number> |
      | artwork_link   | https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/<id>.png |

    Examples: Getting pokemon data with form name
      | name         | form_name    | id    | pokedex_number |
      | deoxys-speed | deoxys-speed | 10003 | 386            |

    Examples: Getting pokemon data with species name when no form corresponds to species name
      | name   | form_name     | id  | pokedex_number |
      | deoxys | deoxys-normal | 386 | 386            |

  Scenario Outline: Getting pokemon from the /pokemon route, species cases, no artwork
    When getting /pokemon/<name>
    Then the following data is received
      | data field     | field value      |
      | name           | <form_name>      |
      | pokedex_number | <pokedex_number> |
      | artwork_link   | None             |

    Examples: Getting
      | name     | form_name | pokedex_number |
      | miraidon | miraidon  | None           |

  @wip
  Scenario Outline: Getting pokemon list from ranges where species based fetching matters
    When getting /pokemon?start=<start>&end=<end>
    Then models named <expected_names> received

    Examples:
      | start | end | expected_names           |
      | 384   | 387 | jirachi, deoxys, turtwig |
