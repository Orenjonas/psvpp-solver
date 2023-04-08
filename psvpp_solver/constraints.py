import numpy as np


def check_constraints_satisfied(schedule,
                                installations,
                                days_in_a_period=[1, 2, 3, 4, 5, 6, 7]):
    """
    Check if the given schedule passes the constraints:
        - Sailling distance?
        - Duration
        - Number of installations
        - Deck capacity
    """

    # (2) Ensure the required service frequency for each installation
    np.sum(voyages_to_i) >= requirements_for_i

    # (3) Ensure PSVs do not sail more days than allowed
    # for duration in possible_durations:
    #     for voyage in (voyages where voyage.duration=duration):
    #         for t in days_in_a_week:

    for voyage in voyages:
        np.sum(voyage_lengths) <= days_chartered_voyages_are_available[voyage]

    # (4) Restict the number of PSVs prepared at the supply depot

    # (5) PSV cannot begin a voyage before returning from its previous one

    # (6) Make sure departures to each installation are properly spread

    # (7) Variable domains


if __name__ == "__main__":

    # Chromosome is schedules of [tour, installations, vessels]
    parent_1 = [
        # tour
        [[[1, 2], [],     [4, 3, 2], []],
         [[],     [3, 4], [],        [1, 2]]
         ],
        # installations
        [[1, 4], [1, 3, 4], [2, 3], [2, 3]],
        # vessels
        [[1, 3], [2, 4]]
    ]

    parent_2 = [
        # tour
        [[[1, 2], [],     [4, 3, 2], []],
         [[],     [3, 4], [],        [1, 2]]
         ],
        # installations
        [[1, 4], [1, 3, 4], [2, 3], [2, 3]],
        # vessels
        [[1, 3], [2, 4]]
    ]

    installations = []
