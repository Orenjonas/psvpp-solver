from IPython import embed
import numpy as np
from numba import njit
import timeit


@njit
def foo(x):
    lst = []
    for j in range(10):
        for i in range(x):
            lst.append([2])
    return lst


@njit
def foo2(x):
    lst = np.array(shape = [[] for i in range(10)]
    for i in range(len(lst)):
        lst[i] = 2  # .append(2)
    return lst


embed()
