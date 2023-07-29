import numpy as np
import random
from itertools import chain


def calculate_cost_of_route(routes: np.ndarray,
                            weekly_charter_costs: np.ndarray,
                            sailing_costs: np.ndarray,
                            distances: np.ndarray) -> float:
    """Calculate the planning periods (e.g. weekly) cost of a schedule based on
    individual vessel costs and sailing distances.

    Args:
        routes (np.array): Sailing routes for the schedule.
        weekly_charter_costs (np.array): One entry for each vessel.
        sailing_costs (np.array): Cost per km. One entry for each vessel.
        distances (np.array): n_installations x n_installations array.
            Each pair contains distance between intallations.
            E.g. installations[i, j] = km between installation i and j.
    Returns:
        np.ndarray: Array of floats, each representing the cost for the
            corresponding vessel.
    """
    # Get index of distances for consecutive installation and depot visits by
    #  padding routes with zero (depot) at the start and end of the schedule
    #  and indexing distances by these padded routes shifted by one day.
    zero_padding = np.zeros_like(routes[:, :, 0:1])  # Get correct dimensions
    total_sailing_distance = np.sum(
        distances[np.concatenate((routes, zero_padding), axis=2),
                  np.concatenate((zero_padding, routes), axis=2)],
        axis=(2, 1))

    # Weekly cost of route is the sum of chartering cost for each vessel, and
    # cost of sailing length for each vessel
    return np.sum(weekly_charter_costs) + np.dot(total_sailing_distance,
                                                 sailing_costs)


def generate_visits(n_installations: int,
                    n_days_in_period: int,
                    required_services=np.array([2, 3, 2, 2], dtype=np.int8),
                    max_vessels_prepared=2) -> np.ndarray:
    """Generate visit days for each installation by randomly assign an
    installation to each installation i.

    With three installations and 7 days visits array can look like this:

        array([[False, False, False,  True, False, False, False],
               [False,  True,  True, False, False, False,  True],
               [ True, False, False,  True,  True,  True,  True]])

    Args:
        required_services (np.array): Array of length n_installations with
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
    visits = np.full((n_installations, n_days_in_period),
                     fill_value=False,
                     dtype=bool)

    # Randomly fill visits for each service frequency requirement
    for inst in range(n_installations):

        # Spread installations by selecting a distance between min and
        # max spread (retry if still not sufficiently spread)
        Pf_max = n_days_in_period // required_services[inst]
        # If division is even, space between services is equal
        if Pf_max == n_days_in_period / required_services[inst]:
            Pf_min = Pf_max = Pf_max - 1
        else:
            Pf_min = Pf_max - 1

        def generate_service_days():
            # Which days should installation i be serviced
            service_days = np.full(shape=required_services[inst],
                                   fill_value=0,
                                   dtype=np.int8)

            while True:
                # Look for equally spaced departures

                # Place first day between 0 and pfmax
                service_days[0] = random.randint(0, Pf_max)

                # If more days, space between is between pf min and pfmax
                if required_services[inst] >= 2:
                    for j in range(1, required_services[inst]):
                        service_days[j] = service_days[j-1] + random.randint(Pf_min,
                                                                             Pf_max) + 1
                # Ensure space between last and first service between Pf_min and Pf_max
                if (Pf_min <= (service_days[0] -
                               (service_days[-1] - (n_days_in_period - 1))) <= Pf_max):
                    break
                else:
                    continue  # If not, try again

            return service_days

        while True:
            # service days may generate days that are too far spread out
            service_days = generate_service_days()

            try:
                # Set chosen service days in boolean visits array
                visits[inst, service_days] = True
                break  # Successfully found properly spread services

            except IndexError:
                pass  # Keep looking for proper service days

    return visits


def generate_departures_from_visits(visits: np.ndarray,
                                    n_vessels: int,
                                    n_installations: int,
                                    n_days_in_period: int) -> np.ndarray:
    """Generate departures for each vessel, ensuring a departure each day that
    requires a visit to a station.

    With four vessels and seven days, departures can look like this:

        array([[ True, False, False, False,  True, False, False],
               [ True, False, False,  True, False,  True, False],
               [False,  True, False, False, False,  True, False],
               [False,  True, False, False, False,  True, False]])

    Args:
        visits (np.ndarray): a
        n_vessels (int): a
        n_installations (int): a
        n_days_in_period (int): a

    Retuns:
        np.ndarray: Boolean array of shape n_vessels, n_days.
        """

    # Initiate departures
    departures = np.zeros(shape=(n_vessels, n_days_in_period),
                          dtype=bool)

    departure_days = visits.any(axis=0)
    departure_days_idx = np.where(departure_days)[0]
    # Ensure each vessel is assigned one departure day
    # Ramdomly sample three days (index)
    assigned_days = np.random.choice(departure_days_idx,
                                     size=np.min([n_vessels,
                                                  len(departure_days_idx)]),
                                     replace=False)

    # Shuffle vessels
    vessels = np.random.choice(range(n_vessels),
                               size=np.min([n_vessels,
                                            len(departure_days_idx)]),
                               replace=False)

    # Set initial departures
    departures[vessels, assigned_days] = 1

    # Randomly assign vessels to remaining departure days
    # Shuffle remaining days
    # remaining_days = np.where(np.delete(departure_days, assigned_days))[0]
    remaining_days = departure_days
    remaining_days[assigned_days] = 0
    remaining_days_idx = np.where(remaining_days)[0]
    assigned_days = np.random.choice(remaining_days_idx,
                                     size=len(remaining_days_idx),
                                     replace=False)

    # Sample vessels for the remaining days with replacement
    vessels = np.random.choice(range(n_vessels), size=len(remaining_days_idx),
                               replace=True)

    # Set remaining departures
    departures[vessels, assigned_days] = 1

    # TODO: implement
    # # Check depot capasity
    # from psvpp_solver.constraints import check_max_pvs_prepared_constraint
    # if not check_max_pvs_prepared_constraint(departures=departures,
    #                                          max_v_prepared=max_v_prepared):
    #     print('too many prepared:')
    #     print(visits*1)

    return departures


# TODO: Update docstring
def generate_routes_from_visits_and_departures(visits: np.ndarray,
                                               departures: np.ndarray,
                                               n_days_in_period: int) -> np.ndarray:
    """Generate routes from visits and departures. The routes contains the
    index of an installation visited by the given vessel on the given day.

    Routes can look like this
    array([[[1, 2, 0, 0],
            [0, 0, 0, 0],
            [4, 3, 2, 0],
            [0, 0, 0, 0]],

           [[0, 0, 0, 0],
            [3, 4, 0, 0],
            [0, 0, 0, 0],
            [1, 2, 0, 0]]])

    Args:

    Returns:
        np.ndarray: Array of shape (n_vessels, n_days, n_installations)
        containing the index of the installation visited by the given vessel
        on the given day"""
    # Assign vessel departures to visits

    # Initiate
    routes = np.zeros(shape=(len(departures), n_days_in_period, len(visits)),
                      dtype=np.int8)

    # Get the index of vessels and index of days they depart
    which_vessel, departure_days = np.where(departures)

    # Get visit days, and which installations are visited a given day
    # TODO: rename
    visit_days, installations_visited = np.where(visits[:, departure_days].T)
    # Installation number is one more than index (0 is depot)
    installations_visited = installations_visited + 1

    # Get number of repeated visit days (several visits in a day) for creation
    # of indexes for these visits
    _, counts = np.unique(visit_days, return_counts=True)

    # Get index of installation visits. Start at zero and count up until the
    # number of visits for each vessel and day using arange()
    installation_order_index = np.fromiter(
        chain.from_iterable(np.arange(x) for x in counts), dtype=np.int8)

    # Duplicate vessel and days with visit_days to set the appropriate indexes
    routes[which_vessel[visit_days],
           departure_days[visit_days],
           installation_order_index] = installations_visited

    return routes


# TODO: Update docstring
def generate_visits_from_routes(routes: np.ndarray,
                                n_installations: int,
                                n_days_in_period: int) -> np.ndarray:
    """Generate genome from journey specifications.

    For example [[[1, 3], [], [2, 4]],
                 [[], [1, 2]]
                 ]

    # tour [PSV][day] -> installations [psv][installation]
    routes = [[[1, 2, 0, 0],
               [0, 0, 0, 0],
               [4, 3, 2, 0],
               [0, 0, 0, 0]],

              [[0, 0, 0, 0],
               [3, 4, 0, 0],
               [0, 0, 0, 0],
               [1, 2, 0, 0]]]

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
    # Initiate boolean array
    installation_visits = np.zeros(shape=(n_installations, n_days_in_period),
                                   dtype=bool)

    for inst in range(n_installations):
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


def initial_population():
    # Individual
    # generate visits

    # Generate departures from visits

    # Check depot capacity
    pass
