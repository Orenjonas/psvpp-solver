import numpy as np


def check_constraints_satisfied(genome,
                                required_frequencies,
                                days_in_period=[1, 2, 3, 4, 5, 6, 7],
                                days_vessel_available=[7, 5],
                                max_installations_visits_in_a_day=3
                                ):
    """
    Check that the given schedule passes the constraints:
        - Sailling distance?
        - Duration
        - Number of installations
        - Deck capacity

    max_installations_visits_in_a_day: int  How many installations can be 
        visited in a day during one voyage. A simplified constraint for distance of voyages.
    """

    # (2) Ensure the required service frequency for each installation
    for i, service_frequencies in enumerate(genome[1]):
        n_visits = len(service_frequencies)
        if n_visits < required_frequencies[i]:
            print('Service frequency for installation', i,
                  'not satisfied')
            return False

    # np.sum(voyages_to_i) >= requirements_for_i

    # (3) Ensure PSVs do not sail more days than allowed
    for duration in possible_durations:
        for voyage in (voyages where voyage.duration=duration):
            for t in days_in_period:
                duration_of_voyage = (
                    (installations_visited-1) // max_installations_visits_in_a_day) + 1

    np.sum(voyage_lengths) <= days_chartered_voyages_are_available[voyage]

    # (4) Restict the number of PSVs prepared at the supply depot

    # (5) PSV cannot begin a voyage before returning from its previous one

    # (6) Make sure departures to each installation are properly spread

    # (7) Variable domains


if __name__ == "__main__":

    genome = [
        # tour [PSV][day]
        [[[1, 2], [],     [4, 3, 2], []],
         [[],     [3, 4], [],        [1, 2]]
         ],
        # installations [instsallation][day visited]
        [[1, 4], [1, 3, 4], [2, 3], [2, 3]],
        # vessels [vessel][day departing]
        [[1, 3], [2, 4]]
    ]

    # installations[installation][required service frequency]
    installation_service_frequencies = [
        1,
        2,
        2,
        3
    ]
