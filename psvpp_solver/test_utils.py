# from psvpp_solver.utils import *
from utils import generate_departures_from_routes, generate_visits_from_routes

import numpy as np

routes = np.array([
    [[1, 2, 0, 0],
     [0, 0, 0, 0],
     [4, 3, 2, 0],
     [0, 0, 0, 0]],
    [[0, 0, 0, 0],
     [3, 4, 0, 0],
     [0, 0, 0, 0],
     [1, 2, 0, 0]]]
)
departures = generate_departures_from_routes(routes=routes)
visits = generate_visits_from_routes(routes,
                                     n_installations=4,
                                     n_days_in_period=4)
print('routes:\n', routes)
print('out:')
print('visits:\n', visits)
print('departures:\n', departures)
