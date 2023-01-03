# Created by MustacheCorp at 03/01/2023
Feature: Fetching pokemon types by name from the route "/type/{name}", hard level
  # TODO explain feature here

  Scenario Outline: Getting a type from the /type route
    When getting /type/<name>
    Then the following data is received
      | data field            | field value               |
      | name                  | <name>                    |
      | id                    | <id>                      |
      | offensive_multipliers | <offensive_multipliers>   |
      | defensive_multipliers | <defensive_multipliers>   |

    Examples: Normal
      | name      | id | offensive_multipliers                     | defensive_multipliers          |
      | normal    | 1  | json({"ghost":0,"rock":0.5,"steel":0.5})  | json({"ghost":0,"fighting":2}) |

    Examples: Ground
      | name      | id | offensive_multipliers                                                                        | defensive_multipliers                                                     |
      | ground    | 5  | json({"flying":0,"bug":0.5,"grass":0.5,"poison":2,"rock":2,"steel":2,"fire":2,"electric":2}) | json({"electric":0,"poison":0.5,"rock":0.5,"water":2,"grass":2,"ice":2})  |

    Examples: Flying
      | name      | id | offensive_multipliers                                                        | defensive_multipliers                                                                  |
      | flying    | 3  | json({"rock":0.5,"steel":0.5,"electric":0.5,"fighting":2,"bug":2,"grass":2}) | json({"ground":0,"fighting":0.5,"bug":0.5,"grass":0.5,"rock":2,"electric":2,"ice":2})  |

    Examples: Electric
      | name      | id | offensive_multipliers                                                            | defensive_multipliers                                       |
      | electric  | 13 | json({"ground":0,"grass":0.5,"electric":0.5,"dragon":0.5,"flying":2,"water":2})  | json({"flying":0.5,"steel":0.5,"electric":0.5,"ground":2})  |
