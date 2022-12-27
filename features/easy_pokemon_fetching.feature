# Created by MustacheCorp at 27/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}", easy features
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # The easy fetching features are returning a list of strings for types of the pokemon and abilities of the pokemon

  Scenario Outline: Getting a pokemon from the /pokemon route with easy feature information
    When getting /pokemon/<name>
    Then the following data is received
      | data field | field value   |
      | types      | [<types>]     |
      | abilities  | [<abilities>] |

    Examples: Murkrow
      | name    | types        | abilities                       |
      | murkrow | dark, flying | insomnia, super-luck, prankster |

    # Add examples here to fill the point requirements

  # Duplicate this if deemed necessary
  Scenario: Getting a random pokemon from the /pokemon route with easy feature information
    When fetching a random pokemon from /pokemon/name
    Then pokemon types and abilities returned