# Created by MustacheCorp at 27/12/2022
Feature: Calculating exp and level changes after winning a battle
  # The backend should have a route for POST "/win-battle" that takes the winning
  # and fainting pokémon in the request body. It should then calculate the level
  # and experience gain if the winning pokémon were to win a fight against the
  # fainted pokémon of given level. 

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
      | level          | 5           |
      | experience     | 128         |

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
      | level          | 9           |
      | experience     | 334         |

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
      | level          | 6           |
      | experience     | 152         |

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
      | level          | 9           |
      | experience     | 412         |


  Scenario: Calculating battle win with winner that does not exist
    Given data
    """
    {
      "winner_name": "winnerman",
      "fainted": {
        "name": "trapinch",
        "level": 13
      }
    }
    """
    When posting /win-battle
    Then 404 is received
