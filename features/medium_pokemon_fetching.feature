# Created by MustacheCorp at 27/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}", medium level features
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # The easy fetching features are returning a list of strings for types of the pokemon and abilities of the pokemon

  Scenario Outline: Getting a pokemon from the /pokemon route with type and ability information
    When getting /pokemon/<name>
    Then the following data is received
      | data field | field value   |
      | types      | [<types>]     |
      | abilities  | [<abilities>] |

    Examples: Murkrow
      | name    | types        | abilities                       |
      | murkrow | dark, flying | insomnia, super-luck, prankster |

    # Add examples here to fill the point requirements

  Scenario Outline: Getting a pokemon from the /pokemon route with stat information
    When getting /pokemon/<name>
    Then the following stats are received
      | name            | value             |
      | hp              | <hp>              |
      | attack          | <attack>          |
      | defense         | <defense>         |
      | special_attack  | <special_attack>  |
      | special_defense | <special_defense> |
      | speed           | <speed>           |

    Examples: Pikachu
      | name    | hp | attack | defense | special_attack | special_defense | speed |
      | pikachu | 35 | 55     | 40      | 50             | 50              | 90    |

  # Duplicate this if deemed necessary
  @wip
  Scenario: Getting a random pokemon from the /pokemon route with type and ability information
    When fetching a random base pokemon from /pokemon/name
    Then pokemon types and abilities returned

  @wip
  Scenario: Getting a random pokemon from the /pokemon route with stat information
    When fetching a random base pokemon from /pokemon/name
    Then pokemon stats returned