import numpy as np
import random


def generate_visits(n_installations: int,
                    n_days: int,
                    required_services=np.array([2, 3, 2, 2], dtype=np.int8),
                    ) -> np.ndarray:
    """Generate visit days for each installation by randomly assign an
    installation to each installation i.

    With three installations and 7 days visits array can look like this:

        array([[False, False, False,  True, False, False, False],
               [False,  True,  True, False, False, False,  True],
               [ True, False, False,  True,  True,  True,  True]])


    Args:
        required_services (np.array): Array of length n_insteallations with
            required service frequencies for each installation.
        n_installations (int): Number of installations
        n_days (int): Number of days in period
        days (np.array): Array of days starting with zero, equivalent to
            range(n_days)

    Returns:
        np.ndarray: Boolean array of size (n_installations, n_days)
                            with visit days set to True.
    """

    # Initialize visits
    visits = np.full((n_installations, n_days),
                     fill_value=False,
                     dtype=bool)

    # Randomly fill visits for each service frequency requirement
    for inst in range(n_installations):

        # Spread installations by selecting a distance between min and
        # max spread (retry if still not sufficiently spread)
        Pf_max = n_days // required_services[inst]
        # If division is even, space between services is equal
        if Pf_max == n_days / required_services[inst]:
            Pf_min = Pf_max = Pf_max - 1
        else:
            Pf_min = Pf_max - 1

        def generate_service_days():
            # Which days should installation i be serviced
            service_days = np.full(shape=required_services[inst],
                                   fill_value=0,
                                   dtype=np.int8)

            while True:
                # Place first day between 0 and pfmax
                service_days[0] = random.randint(0, Pf_max)

                # If more days, space between is between pf min and pfmax
                if required_services[inst] >= 2:
                    for j in range(1, required_services[inst]):
                        service_days[j] = service_days[j-1] + random.randint(Pf_min,
                                                                             Pf_max) + 1
                # Ensure space between last and first service between Pf_min and Pf_max
                if (Pf_min <= (service_days[0] -
                               (service_days[-1] - (n_days - 1))) <= Pf_max):
                    break
                else:
                    continue  # If not, try again

            return service_days

        while True:
            service_days = generate_service_days()

            # service days may generate days that are too far spread out
            try:
                # Set chosen service days in boolean visits array
                visits[inst, service_days] = True
                break  # Successfully found properly spread services
            except IndexError:
                pass  # Keep looking for proper service days

    return visits


def generate_departures_from_visits(visits: np.ndarray,
                                    ) -> np.ndarray:
    pass


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
