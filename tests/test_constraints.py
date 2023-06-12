# from utils import generate_departures_from_routes, generate_visits_from_routes
from psvpp_solver.constraints import check_constraints_satisfied
from psvpp_solver.utils import generate_visits_from_routes
from psvpp_solver.utils import generate_departures_from_routes
from psvpp_solver.visualize_route import visualize_route
import numpy as np


def test_constraints():
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
