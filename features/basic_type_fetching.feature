# Created by MustacheCorp at 03/01/2023
Feature: Fetching pokemon types by name from the route "/type/{name}", basic level
  # The basic type fetching feature fetches only the id and name of types.  

  Scenario Outline: Getting a type from the /type route
    When getting /type/<name>
    Then the following data is received
      | data field    | field value   |
      | name          | <name>        |
      | id            | <id>          |

    Examples: Normal
      | name      | id |
      | normal    | 1  |

    Examples: Ground
      | name      | id |
      | ground    | 5  |

    Examples: Flying
      | name      | id |
      | flying    | 3  |

    Examples: Electric
      | name      | id |
      | electric  | 13 |
