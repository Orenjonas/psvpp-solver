
def check_constraints_satisfied(
    genome: list[list[int]],
    # TODO - change to len(period)
    days_in_period=[1, 2, 3, 4, 5, 6, 7],
    days_vessel_available: list[int] = [7, 5],
    max_v_prepared: list[int] = [2, 2, 2, 2, 2, 1, 1],
    max_psv_prepared_per_day: int = 2,
    departures_each_day: list[int] = [0, 0, 0, 0, 0, 0, 0],
        required_frequencies: list[int] = [2, 3, 2, 2]) -> bool:
    """
    Check that the given schedule passes the given constraints.

     Constraints:
        - Sailling distance?
        - Duration
        - Number of installations
        - Deck capacity
        For all periodic supply vessels (PSVs)

    Args:
        genome: TODO
        required_frequencies
        max_installations_visits_in_a_day (int):  How many installations can
            be visited in a day during one voyage. A simplified constraint for
            distance of voyages.
        max_v_prepared (list[int]): How many vessels the installations can
            prepare for departure in day i, list of len n_days.
    """
    # (2) Ensure the required service frequency for each installation
    for inst, services in enumerate(genome[1]):
        n_visits = len(services)
        if n_visits < required_frequencies[inst]:
            print('Service frequency for installation', inst,
                  'not satisfied')
            print("Genome:", genome)
            return False

    # (3) Ensure PSVs do not sail more days than allowed

    for psv, voyages in enumerate(genome[0]):
        len_voyages = 0

        for voyage in voyages:
            len_voyages += len(voyage)

        if len_voyages > days_vessel_available[psv]:
            print('Constraint not satisfied: Supply vessel {psv} sails '
                  '{len_voyages} days but is available only {max_days} days'
                  '.'.format(psv=psv,
                             max_days=days_vessel_available[psv],
                             len_voyages=len_voyages)
                  )
            print("Genome:", genome)
            return False

    # (4) Restict the number of PSVs prepared at the supply depot
    for psv, departures in enumerate(genome[2]):
        for day in departures:
            # Day starts count on 1. List index will be `day-1`
            departures_each_day[day-1] += 1
            if departures_each_day[day] > max_psv_prepared_per_day:
                print('Too many vessels serviced on day', day)
                print("Genome:", genome)
                return False

    # (5) PSV cannot begin a voyage before returning from its previous one
    prev_depart = None
    for psv, departures in enumerate(genome[2]):

        # First check difference between last and first departure in the period
        prev_depart = departures[-1] - len(days_in_period)
        for departure_day in departures:
            # Assumes all journeys are 1 day long and can sail the day after
            # returning.

            # Check that there is one day between departures
            if departure_day - prev_depart < 1:
                print("Not enough time between journeys departing on day "
                      "{prev_depart} and {departure_day}, for psv {psv}"
                      ".".format(prev_depart=prev_depart,
                                 departure_day=departure_day,
                                 psv=psv,)
                      )
                print("Genome:", genome)
                return False
            prev_depart = departure_day

    # (6) Make sure departures to each installation are properly spread
    for inst, services in enumerate(genome[1]):
        # Min and max distance between visits
        f = required_frequencies[inst]
        # df = len(days_in_period) / (f+1)
        Pf_min = len(days_in_period) // (f+1)
        Pf_max = Pf_min + 1
        # Pf_min = f // df
        # Pf_max = f // df + 1

        # TODO: check [3, 4] and [1,3,4]

        # What if only one visit? [1]

        prev = services[-1] - len(days_in_period)
        for day in services:
            # Check diff within constraints
            # TODO: Check definition of time between visits
            days_between = day - prev - 1  # Number of days between services
            if days_between < Pf_min or days_between > Pf_max:
                # from IPython import embed
                # embed()
                print('day', day, 'prev', prev)
                print('Services not sufficiently spread for  installation', inst)
                print("Genome:", genome)
                return False

            prev = day

    # (7) Variable domains


if __name__ == "__main__":

    #     genome = [
    #         # tour [PSV][day] -> installations
    #         [[[1, 2], [],     [4, 3, 2], []],
    #          [[],     [3, 4], [],        [1, 2]]
    #          ],
    #         # installations [instsallation] -> day visited
    #         [[1, 4], [1, 3, 4], [2, 3], [2, 3]],
    #         # vessels [vessel] -> day departing
    #         [[1, 3], [2, 4]]
    #     ]

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

    # installations[installation][required service frequency]
    installation_service_frequencies = [
        1,
        2,
        2,
        3
    ]

    check_constraints_satisfied(genome)
