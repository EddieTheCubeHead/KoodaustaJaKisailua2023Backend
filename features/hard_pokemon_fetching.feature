# Created by MustacheCorp at 27/12/2022
Feature: Fetching pokemon by name from the route "/pokemon/{name}", medium features
  # The backend should have the route "/pokemon/{name}" that allows fetching pokemon data by nane
  # The easy fetching features are returning a list of strings for types of the pokemon and abilities of the pokemon

  Scenario: Getting happiness evolution information
    When getting /pokemon/snorlax
    Then the following evolution chain is received
    """
    munchlax, 446, , [snorlax]
    snorlax, 143, Level up while happiness is over 160, []
    """

    # Add examples here to fill the point requirements