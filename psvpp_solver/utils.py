import numpy as np


def generate_visits(n_installations: int,
                    n_days: int,
                    days: np.array,
                    service_frequencies=np.array([2, 3, 2, 2], dtype=np.int8),
                    ) -> np.ndarray:
    """Generate visit days for each installation by randomly assign an
    installation to each installation i.

    With three installations and 7 days visits array can look like this:

        array([[False, False, False,  True, False, False, False],
           [False,  True,  True, False, False, False,  True],
           [ True, False, False,  True,  True,  True,  True]])


    Args:
        service_frequencies (np.array): Array of length n_insteallations with
            required service frequencies for each installation.
        n_installations (int): Number of installations
        n_days (int): Number of days in period
        days (np.array): Array of days starting with zero, equivalent to
            range(n_days)

    Returns:
        np.ndarray: Boolean array of size (n_installations, n_days)
                            with visit days set to True.
    """
    rng = np.random.default_rng()

    # Initialize visits
    visits = np.zeros((n_installations, n_days), dtype=bool)

    # Randomly fill visits for each service frequency requirement
    for i in range(n_installations):
        visit_days = rng.choice(days,
                                size=service_frequencies[i],
                                replace=False
                                )
        visits[i, visit_days] = True

    return visits


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
                                     dtype=bool)

    for inst in range(n_installations):
        # TODO: Check if more than one visit to same installation in a day?
        installation_visits[inst] = (routes == (inst + 1)).any(axis=(0, 2))

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

    return np.array(routes[:, :, 0] > 0, dtype=bool)
