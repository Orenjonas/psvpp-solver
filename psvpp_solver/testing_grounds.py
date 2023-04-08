import itertools
from numpy.random import default_rng
import numpy as np

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

# CROSSOVER OPERATOR

# Setup
vessels = [1, 2, 3]
days = [1, 2, 3, 4, 5, 6, 7]

# STEP 0: INHERITANCE RULE
# 2. Pick two random integer numbers between 0 and |T| × |V|
rng = default_rng()
d_x_v = len(days) * len(vessels)
cutoff = rng.integers(low=0, high=d_x_v, size=2)

n1 = cutoff.min()
n2 = cutoff.max()

vessels_shuffeled = rng.choice(vessels, size=len(vessels), replace=False)
days_shuffeled = rng.choice(days, size=len(days), replace=False)

# Combinations of vessels and days (slice to select the sets for crossover)
DxV = list(itertools.product(vessels_shuffeled, days_shuffeled))


# STEP 1: Inherit data from s1
for v, d in itertools.islice(DxV, 0, n1):
    # 7. Copy the sequence of installation departures from parent1 to sibling
    print(v, d)


# for vessel in range(len(vessels_shuffeled):
#                     days_shuffeled[i,:] = rng.choice(days, size=len(days), )
