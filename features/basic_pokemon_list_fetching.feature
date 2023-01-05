# Created by MustacheCorp at 04/01/2023
Feature: Fetching a list of pokemons from the route "/pokemon", basic level
    # The pokemon list feature fetches a list of pokemon with given pokedex
    # number limits.


    Scenario: Getting a list of pokemons with default parameters
        When getting /pokemon
        Then list features/data/pokemon_list_first_10.json is received
        And the length of the list is 10
    

    Scenario Outline: Getting a list of pokemons
        When getting /pokemon?start=<start>&end=<end>
        Then list <json file> is received
        And the length of the list is <length>

        Examples: Subset 45 to 58
            | start | end   | json file                                 | length    |
            | 44    | 58    | features/data/pokemon_list_45_to_58.json  | 14        |

        Examples: Only 453
            | start | end | json file                           | length    |
            | 452   | 453 | features/data/pokemon_list_453.json | 1         |


    Scenario: Getting a list of pokemons with start greater than end
        When getting /pokemon?start=968&end=967
        Then the length of the list is 0