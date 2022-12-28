# Created by MustacheCorp at 27/12/2022
Feature: Calculating exp and level changes after winning a battle
  # TODO explain feature here

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

  @wip
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


