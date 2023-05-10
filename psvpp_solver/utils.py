import numpy as np


def generate_visits_from_routes(routes: np.ndarray,
                                n_installations: int,
                                n_days_in_period: int) -> np.ndarray:
    """Generate genome from journey specifications.

    For example [[[1, 3], [], [2, 4]],
                 [[], [1, 2]]
                 ]

    # tour [PSV][day] -> installations [psv][installation]
    routes = [[
        [[1, 2, 0, 0], # [[1, 2], [],     [4, 3, 2], []],
         [0, 0, 0, 0],
         [4, 3, 2, 0]
         [0, 0, 0, 0]]
        [[0, 0, 0, 0], # [[],     [3, 4], [],        [1, 2]]
         [3, 4, 0, 0],
         [0, 0, 0, 0],
         [1, 2, 0, 0]]

            # installations [installation] -> day visited
    installation_visits = [
            [1, 0, 0, 1, 0, 0, 0], # [1, 4]
            [1, 3, 5],
            [2, 3],
            [2, 3]],
    # vessels [vessel] -> day departing
    departure_days = [[1, 0, 0, 1],  # [[1, 4], [2, 4]]
                      [0, 1, 0, 1]]
    """
    installation_visits = np.ndarray(shape=(n_installations, n_days_in_period),
                                     dtype=int)

    for inst in range(n_installations):
        # TODO: Check if more than one visit to same installatio in a day?
        installation_visits[inst] = (routes == inst).any(axis=(0, 2))

    return installation_visits


def generate_departures_from_routes(routes: np.ndarray) -> np.ndarray:
    """Generate genome from journey specifications.

    For example [[[1, 3], [], [2, 4]],
                 [[], [1, 2]]
                 ]

    # tour [PSV][day] -> installations [psv][installation]
    routes = [[
        [[1, 2, 0, 0], # [[1, 2], [],     [4, 3, 2], []],
         [0, 0, 0, 0],
         [4, 3, 2, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0], # [[],     [3, 4], [],        [1, 2]]
         [3, 4, 0, 0],
         [0, 0, 0, 0],
         [1, 2, 0, 0]]

            # installations [installation] -> day visited
    installation_visits = [
            [1, 0, 0, 1, 0, 0, 0], # [1, 4]
            [1, 0, 1, 0, 1, 0, 0], # [1, 3, 5]
            [0, 1, 1, 0, 0, 0, 0], # [2, 3,
            [0, 1, 1, 0, 0, 0, 0]] # [2, 3]
    # vessels [vessel] -> day departing
    departure_days = [[1, 0, 0, 1],  # [1, 4]
                      [0, 1, 0, 1]]  # [2, 4]
    """
    # departure_days = np.darray(shape=(n_vessels, n_days_in_period),
    #                             dtype=bool)
    departure_days = np.array(routes[:, :, 0] > 0, dtype=bool)

    return departure_days
