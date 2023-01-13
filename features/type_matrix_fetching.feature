# Created by MustacheCorp at 10/01/2023
Feature: Fetching type matchup matrix from /types
  # Fetching /types should return a matrix of type matchups. The matrix should contain a top row of all type names
  # and then a row for every type in the top row in order containing the offensive multipliers for said type for the
  # types in top row order

  Scenario: Getting type matrix from /types. Contains all required types and no extra types
    When getting /types
    Then received type matrix that contains the following types and only the following types
    """
    normal, fire, water, grass, electric, ice, fighting, poison, ground, flying, psychic, bug, rock, ghost, dark,
    dragon, steel, fairy
    """

  Scenario: Getting type matrix from /types. All rows have correct number of multipliers
    When getting /types
    Then received type matrix where every matchup row has 18 multipliers

  Scenario: Getting type matrix from /types. All types have correct multipliers
    When getting /types
    Then every row of the received type matrix should have the correct multipliers for the type it represents