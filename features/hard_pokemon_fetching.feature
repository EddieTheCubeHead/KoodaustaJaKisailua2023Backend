# Created by MustacheCorp at 27/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}", medium features
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # The easy fetching features are returning a list of strings for types of the pokemon and abilities of the pokemon

  Scenario: Getting level up evolution information
    When getting /pokemon/gabite
    Then the following evolution chain is received
    """
    gible, 443, , [gabite]
    gabite, 444, Level up while level is at least 24, [garchomp]
    garchomp, 445, Level up while level is at least 48, []
    """

  Scenario: Getting happiness evolution information
    When getting /pokemon/snorlax
    Then the following evolution chain is received
    """
    munchlax, 446, , [snorlax]
    snorlax, 143, Level up while happiness is at least 160, []
    """

  Scenario: Getting branching evolution information
    When getting /pokemon/eevee
    Then the following evolution chain is received
    """
    eevee, 133, , [vaporeon, jolteon, flareon, espeon, umbreon, leafeon, glaceon, sylveon]
    vaporeon, 134, Use the item Water Stone, []
    jolteon, 135, Use the item Thunder Stone, []
    flareon, 136, Use the item Fire Stone, []
    espeon, 196, Level up while happiness is at least 160 and it is day, []
    umbreon, 197, Level up while happiness is at least 160 and it is night, []
    leafeon, 470, Level up while in Eterna Forest, []
    glaceon, 471, Level up while in Route 217, []
    sylveon, 700, Level up while knowing a fairy-type move and affection is at least 2, []
    """

  Scenario: Getting gender dependent evolution information
    When getting /pokemon/ralts
    Then the following evolution chain is received
    """
    ralts, 280, , [kirlia]
    kirlia, 281, Level up while level is at least 20, [gardevoir, gallade]
    gardevoir, 282, Level up while level is at least 30, []
    gallade, 475, Use the item Dawn Stone while being male, []
    """

  Scenario: Getting trading evolution information
    When getting /pokemon/machoke
    Then the following evolution chain is received
    """
    machop, 66, , [machoke]
    machoke, 67, Level up while level is at least 28, [machamp]
    machamp, 68, Trade, []
    """

  Scenario: Getting trading while holding item evolution information
    When getting /pokemon/porygon-z
    Then the following evolution chain is received
    """
    porygon, 137, , [porygon2]
    porygon2, 233, Trade while is holding the item Upgrade, [porygon-z]
    porygon-z, 474, Trade while is holding the item Dubious Disc, []
    """
