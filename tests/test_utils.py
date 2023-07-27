from psvpp_solver.utils import calculate_cost_of_route
from psvpp_solver.utils import generate_departures_from_routes
from psvpp_solver.utils import generate_departures_from_visits
from psvpp_solver.utils import generate_visits_from_routes
from psvpp_solver.utils import generate_visits
from psvpp_solver.constraints import check_constraints_satisfied
import numpy as np


def test_calculate_cost_of_route():

    # Initiate
    routes = np.array([[[1, 2, 0, 0],
                        [0, 0, 0, 0],
                        [4, 3, 2, 1],
                        [0, 0, 0, 0]],
                       [[0, 0, 0, 0],
                        [3, 4, 0, 0],
                        [0, 0, 0, 0],
                        [1, 2, 0, 0]]])

    distances = np.array([[0, 1, 2, 3, 4],
                          [0, 0, 5, 6, 4],
                          [0, 0, 0, 7, 4],
                          [0, 0, 0, 0, 4],
                          [0, 0, 0, 0, 0]])
    distances = distances + distances.T

    cost_of_route = calculate_cost_of_route(routes=routes,
                                            weekly_charter_costs=np.array(
                                                (100000.0,
                                                 150000.0)),
                                            sailing_costs=np.array((1000,
                                                                    1200)),
                                            distances=distances)
    assert cost_of_route == 301800.0


def test_generate_departures_from_visits():

    for n_installations in range(2, 10):
        for n_days_in_period in range(4, 14):
            for n_vessels in range(np.min([n_installations, n_days_in_period]),
                                   np.max([n_installations, n_days_in_period])):
                for i in range(100):
                    required_services = np.random.choice(
                        range(1, n_days_in_period // 2),
                        size=n_installations,
                        replace=True)

                    visits = generate_visits(n_installations=n_installations,
                                             n_days_in_period=n_days_in_period,
                                             required_services=required_services
                                             )
                    departures = generate_departures_from_visits(visits=visits,
                                                                 n_vessels=n_vessels,
                                                                 n_installations=n_installations,
                                                                 n_days_in_period=n_days_in_period)
                    assert np.array_equal(departures.any(axis=0),
                                          visits.any(axis=0)), f'generate_departures_from_visits does not meet visit requirements for {n_vessels} vessels, {n_installations} installations and a {n_days_in_period} day period. \n\nvisits:\n{visits*1}\n\ndepartures:\n{departures*1} \n\nrequired services:\n{required_services}'


def test_check_constraints_satisfied():
    routes = np.array([[[1, 2, 3, 4],
                        [0, 0, 0, 0],
                        [4, 2, 0, 0],
                        [0, 0, 0, 0]],

                       [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [3, 0, 1, 0],
                        [2, 0, 0, 0]]])
    visits = generate_visits_from_routes(routes,
                                         n_installations=4,
                                         n_days_in_period=4)
    departures = generate_departures_from_routes(routes)
    result = check_constraints_satisfied(routes,
                                         visits,
                                         departures,
                                         required_services=np.array(
                                             [2, 3, 2, 2]),
                                         max_v_prepared=np.array([2, 2, 2, 1]),
                                         n_days_available=np.array([2, 3]),
                                         days_in_period=4,
                                         )

    assert result is True, "Constraints should be satisfied for:\n{}".format(
        routes
    )


def test_generate_departures_from_routes():
    pass


def test_generate_visits_from_routes():
    pass


def test_generate_visits():
    pass
