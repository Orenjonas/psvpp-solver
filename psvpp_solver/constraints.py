# from threading import enumerate


def check_constraints_satisfied(
        genome: list[list[int]],
        required_frequencies,
        days_in_period=[1, 2, 3, 4, 5, 6, 7],
        days_vessel_available: list[int] = [7, 5],
        max_v_prepared: list[int] = [
            2, 2, 2, 2, 2, 2, 2],
        max_psv_prepared_per_day: int = 2,
        departures_each_day: list[int] = [0, 0, 0, 0, 0, 0, 0]) -> bool:
    """ Check that the given schedule passes the constraints:
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
    for i, service_frequencies in enumerate(genome[1]):
        n_visits = len(service_frequencies)
        if n_visits < required_frequencies[i]:
            print('Service frequency for installation', i,
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
        first_depart = departures[0]
        last_depart = departures[-1]
        if first_depart <= (last_depart + 1) % len(days_in_period):
            print("Not enough time between journeys departing on day"
                  "{first_depart} and {last_depart}, for psv {psv}"
                  ".".format(first_depart=first_depart,
                             last_depart=last_depart,
                             psv=psv,)
                  )
            print("Genome:", genome)
            return False

        # TODO: Check boundary (check only one departure)

        for departure_day in departures:
            # Assumes all journeys are 1 day long and requires one day between
            # returning and starting a new journey.
            if prev_depart is not None:
                # Check that there is one day between departures
                if departure_day - prev_depart < 2:
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

        # (7) Variable domains


if __name__ == "__main__":

    genome = [
        # tour [PSV][day] -> installations
        [[[1, 2], [],     [4, 3, 2], []],
         [[],     [3, 4], [],        [1, 2]]
         ],
        # installations [instsallation] -> day visited
        [[1, 4], [1, 3, 4], [2, 3], [2, 3]],
        # vessels [vessel] -> day departing
        [[1, 3], [2, 4]]
    ]

    # installations[installation][required service frequency]
    installation_service_frequencies = [
        1,
        2,
        2,
        3
    ]
