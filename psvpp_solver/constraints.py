import numpy as np


# TODO: docstring and type hints
# TODO: numba function?
def check_departures_sufficiently_spread(visits,
                                         days_in_period: int,
                                         required_services,
                                         routes="",
                                         departures="",
                                         print_output=False
                                         ):
    # (6) Make sure departures to each installation are properly spread
    for inst, services in enumerate(visits):

        # Translate to day visited
        services = np.where(services)[0]

        # Min and max distance between visits
        Pf_max = days_in_period // required_services[inst]
        # If division is even, space between services is equal
        if Pf_max == n_days / required_services[inst]:
            Pf_min = Pf_max = Pf_max - 1
        else:
            Pf_min = Pf_max - 1

        prev = services[-1] - days_in_period
        for day in services:
            # Check diff within constraints
            days_between = day - prev - 1  # Number of days between services
            if days_between < Pf_min or days_between > Pf_max:
                if print_output:
                    print('day', day, 'prev', prev)
                    print('Services not sufficiently spread for  installation',
                          inst + 1)
                    if routes != "":
                        print("routes", routes, sep="\n")
                    print("visits", visits*1, sep="\n")
                    if departures != "":
                        print("departures", departures*1, sep="\n")
                return False

            prev = day
        # TODO: Check spread between last and first service day
    return True


def check_correct_service_frequencies(visits,
                                      required_services,
                                      departures,
                                      routes):
    # TODO: docstring and type hints
    # (2) Ensure the correct service frequency for each installation

    if (not np.array_equal(visits.sum(axis=1),  # visit frequency
                           required_services)):
        # Abort if service frequency requirement not correct.
        print('Service frequency for installation(s)',
              np.where(~np.equal(visits.sum(axis=1),
                       required_services))[0] + 1,
              'not correct')
        print("routes", routes,
              "visits", visits*1,
              "departures", departures*1,
              sep="\n"
              )
        return False
    return True


def check_max_sailing_days_constraint(n_days_available,
                                      routes,
                                      visits,
                                      departures):
    # TODO: docstring and type hints

    # (3) Ensure PSVs do not sail more days than allowed
    # Assumes any voyage takes one day
    days_chartered = np.array(routes[:, :, 0] > 0, dtype=bool).sum(axis=1)

    if (np.any(days_chartered > n_days_available)):

        print('Vessel(s)',
              np.where(days_chartered > n_days_available)[0] + 1,
              'sails more days than they are available.')
        print("routes", routes,
              "visits", visits*1,
              "departures", departures*1,
              sep="\n"
              )
        return False
    return True


def check_pax_pvs_prepared_constraint(departures,
                                      max_v_prepared,
                                      routes,
                                      visits,
                                      ):
    # (4) Restict the number of PSVs prepared at the supply depot
    if np.any(departures.sum(axis=0) > max_v_prepared):
        print('Too many departures on day(s))',
              np.where(departures.sum(axis=0) > max_v_prepared)[0] + 1)
        print("routes", routes,
              "visits", visits*1,
              "departures", departures*1,
              sep="\n"
              )
        return False
    return True


def check_voyages_dont_overlap(departures,
                               days_in_period,
                               routes,
                               visits):
    # (5) PSV cannot begin a voyage before returning from its previous one
    prev_depart = None
    for vessel, departures_v in enumerate(departures):
        # Translate to day of departure
        departures_v = np.where(departures_v)[0]
        prev_depart = departures_v[-1] - days_in_period
        for departure_day in departures_v:
            # Assumes all journeys are 1 day long and can sail the day after
            #  returning.

            # Check that there is one day between departures
            if departure_day - prev_depart < 1:
                print("Not enough time between journeys departing on day "
                      "{prev_depart} and {departure_day}, for psv {vessel}"
                      ".".format(prev_depart=prev_depart + 1,
                                 departure_day=departure_day + 1,
                                 vessel=vessel + 1,)
                      )
                print("routes", routes,
                      "visits", visits*1,
                      "departures", departures*1,
                      sep="\n"
                      )
                return False

            prev_depart = departure_day
    return True


def check_constraints_satisfied(
        routes: np.ndarray,
        visits: np.ndarray,
        departures: np.ndarray,
        required_services=np.array([2, 3, 2, 2]),
        max_v_prepared=np.array([2, 2, 2, 1]),
        n_days_available=np.array([2, 2]),
        days_in_period=4,
) -> bool:
    """Check that the given schedule passes the given constraints.

        routes =  [[[1 2 0 0]
                    [0 0 0 0]
                    [4 3 2 0]
                    [0 0 0 0]]

                   [[0 0 0 0]
                    [3 4 0 0]
                    [0 0 0 0]
                    [1 2 0 0]]]

         visits = [[1 0 0 1]
                   [1 0 1 1]
                   [0 1 1 0]
                   [0 1 1 0]]
         departures = [[1 0 1 0]
                       [0 1 0 1]]

     Constraints:
         - Sailling distance?
        - Duration
        - Number of installations
        - Deck capacity
        For all periodic supply vessels (PSVs)


    Args:
        genome: TODO
        required_services
        max_installations_visits_in_a_day (int):  How many installations can
            be visited in a day during one voyage. A simplified constraint for
            distance of voyages.
        max_v_prepared (list[int]): How many vessels the installations can
            prepare for departure in day i, list of len n_days.
    """
    if not check_correct_service_frequencies(visits,
                                             required_services,
                                             departures,
                                             routes):
        return False

    if not check_max_sailing_days_constraint(n_days_available,
                                             routes,
                                             visits,
                                             departures):
        return False

    if not check_pax_pvs_prepared_constraint(departures,
                                             max_v_prepared,
                                             routes,
                                             visits
                                             ):
        return False

    if not check_voyages_dont_overlap(departures,
                                      days_in_period,
                                      routes,
                                      visits):
        return False

    if not (check_departures_sufficiently_spread(visits,
                                                 days_in_period,
                                                 required_services,
                                                 routes,
                                                 departures)):
        return False

    # All checks pass
    return True
