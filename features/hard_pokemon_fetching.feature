# Created by MustacheCorp at 27/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}", medium features
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # The hard fetching feature is fetching the evolution data of the pokemon

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
    sylveon, 700, Level up while knowing a Fairy type move and affection is at least 2, []
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

  Scenario: Getting trading with a specific pokemon evolution information
    When getting /pokemon/shelmet
    Then the following evolution chain is received
    """
    shelmet, 616, , [accelgor]
    accelgor, 617, Trade while the other traded pokemon is Karrablast, []
    """

  Scenario: Getting upside down evolution information
    When getting /pokemon/malamar
    Then the following evolution chain is received
    """
    inkay, 686, , [malamar]
    malamar, 687, Level up while level is at least 30 and the console is held upside down, []
    """

  Scenario: Getting beauty evolution information
    When getting /pokemon/milotic
    Then the following evolution chain is received
    """
    feebas, 349, , [milotic]
    milotic, 350, Level up while beauty is at least 171, []
    """

  Scenario: Getting known move evolution information
    When getting /pokemon/piloswine
    Then the following evolution chain is received
    """
    swinub, 220, , [piloswine]
    piloswine, 221, Level up while level is at least 33, [mamoswine]
    mamoswine, 473, Level up while knowing the move Ancient Power, []
    """

  Scenario: Getting pokemon in party evolution information
    When getting /pokemon/mantyke
    Then the following evolution chain is received
    """
    mantyke, 458, , [mantine]
    mantine, 226, Level up while having Remoraid in the party, []
    """

  Scenario: Getting shed trigger evolution information
    When getting /pokemon/nincada
    Then the following evolution chain is received
    """
    nincada, 290, , [ninjask, shedinja]
    ninjask, 291, Level up while level is at least 20, []
    shedinja, 292, Have a free slot in your party and at least one poke ball while evolving Nincada into Ninjask, []
    """

  Scenario: Getting pokemon type in party evolution information
    When getting /pokemon/pangoro
    Then the following evolution chain is received
    """
    pancham, 674, , [pangoro]
    pangoro, 675, Level up while level is at least 32 and having a Dark type pokemon in the party, []
    """

  Scenario: Getting overworld weather evolution information
    When getting /pokemon/sliggoo
    Then the following evolution chain is received
    """
    goomy, 704, , [sliggoo]
    sliggoo, 705, Level up while level is at least 40, [goodra]
    goodra, 706, Level up while level is at least 50 and it is raining, []
    """

  Scenario: Getting stat dependant evolution information
    When getting /pokemon/tyrogue
    Then the following evolution chain is received
    """
    tyrogue, 236, , [hitmonlee, hitmonchan, hitmontop]
    hitmonlee, 106, Level up while level is at least 20 and attack is greater than defence, []
    hitmonchan, 107, Level up while level is at least 20 and attack is smaller than defence, []
    hitmontop, 237, Level up while level is at least 20 and attack is equal to defence, []
    """

  Scenario: Getting randomly branching evolution information
    When getting /pokemon/wurmple
    Then the following evolution chain is received
    """
    wurmple, 265, , [silcoon, cascoon]
    silcoon, 266, Level up while level is at least 7, [beautifly]
    beautifly, 267, Level up while level is at least 10, []
    cascoon, 268, Level up while level is at least 7, [dustox]
    dustox, 269, Level up while level is at least 10, []
    """

  Scenario: Getting spin trainer evolution information
    When getting /pokemon/milcery
    Then the following evolution chain is received
    """
    milcery, 868, , [alcremie]
    alcremie, 869, Spin, []
    """

  Scenario: Getting trigger specific location evolution information
    When getting /pokemon/kubfu
    Then the following evolution chain is received
    """
    kubfu, 891, , [urshifu]
    urshifu, 892, Train in the Tower of Darkness, []
    """

  Scenario: Getting land critical hits evolution information
    When getting /pokemon/farfetchd
    Then the following evolution chain is received
    """
    farfetchd, 83, , [sirfetchd]
    sirfetchd, 865, Land three critical hits in a battle, []
    """

  Scenario: Getting take damage and go to location evolution information
    When getting /pokemon/cofagrigus
    Then the following evolution chain is received
    """
    yamask, 562, , [cofagrigus, runerigus]
    cofagrigus, 563, Level up while level is at least 34, []
    runerigus, 867, Go somewhere after taking damage, []
    """
