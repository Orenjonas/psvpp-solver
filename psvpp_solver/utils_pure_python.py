from numba import int64, njit
from numba.typed import List


@njit
def create_genome(routes: list[list[int]]) -> list[list[list[list[int]]],
                                                   list[list[int]],
                                                   list[list[int]]]:
    """Generate genome from journey specifications.

    For example [[[1, 3], [], [2, 4]],
                 [[], [1, 2]]
                 ]

    genome = [
            # tour [PSV][day] -> installations
            [[[1, 2], [],     [4, 3, 2], []],
             [[],     [3, 4], [],        [1, 2]]
             ],
            # installations [instsallation] -> day visited
            [[1, 4], [1, 3, 5], [2, 3], [2, 3]],
            # vessels [vessel] -> day departing
            [[1, 4], [2, 4]]
            ]
    """
    n_vessels = len(routes)
    # Initiate empty list of departure days
    installation_count = 0

    # Find number of installations as the highest numbered installation
    for psv, journeys in enumerate(routes):
        # [[1, 2], [], [4, 3, 2], []]

        for day, journey in enumerate(journeys):
            # [1, 2]

            for installation in journey:
                if installation > installation_count:
                    installation_count = installation

    # Initiate empty list with number for numba type recognition)
    # Then pop to empty list (found no other way to type empty nested lists)
    installation_visits = [[0] for _ in range(installation_count)]
    for sublist in installation_visits:
        sublist.pop()

    departure_days = [[0] for _ in range(n_vessels)]
    for sublist in departure_days:
        sublist.pop()

    # Build visit days and departure days for genome
    for psv, journeys in enumerate(routes):
        # [[1, 2], [], [4, 3, 2], []]

        for day, journey in enumerate(journeys):
            # [1, 2]
            if (len(journey) != 0):
                departure_days[psv].append(day + 1)

            for installation in journey:
                # days numerated one more than index
                installation_visits[installation - 1].append(day + 1)

    return [routes, sorted(installation_visits), departure_days]


if __name__ == "__main__":
    routes = [[[1, 2], [],     [4, 3, 2], []],
              [[],     [3, 4], [],        [1, 2]]
              ]
    for gene in create_genome(routes):
        print(gene)
