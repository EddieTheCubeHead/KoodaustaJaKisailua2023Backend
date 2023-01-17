# Created by MustacheCorp at 17/01/2023
Feature: Error handling in the server
  # The server should return 404 when given variables for name search or the route itself are unavailable

  Scenario: Getting a pokemon that does not exist
    When getting /pokemon/pikacu
    Then 404 is received


  Scenario: Getting a type that does not exist
    When getting /type/kaiffari
    Then 404 is received

  Scenario: Calculating battle win with fainted that does not exist
    Given data
    """
    {
      "winner_name": "bulbasaur",
      "fainted": {
        "name": "pikacu",
        "level": 5
      }
    }
    """
    When posting /win-battle
    Then 404 is received

  Scenario: Calculating battle win with winner that does not exist
    Given data
    """
    {
      "winner_name": "bulbasaurus",
      "fainted": {
        "name": "pikachu",
        "level": 5
      }
    }
    """
    When posting /win-battle
    Then 404 is received

  Scenario: Fetching unavailable route
    When a non-documented api endpoint is fetched
    Then 404 is received for every fetch attempt
