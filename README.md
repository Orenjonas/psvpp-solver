# Periodic Supply Vessel Planning Problem solver

Implementing solvers for finding optimal planning schedules for periodic supply vessels based on research on the field.

Currently implementing a solution for finding the optimal amount of supply vessels and corresponding optimal sailing schedule for rigs based on supply demand.

Based on the paper by Borthen, Thomas, et al. [[1]](#1).


# Data structures
## Routes
array of shape (number of vessels, number of days in schedule, number of installations)
representing on which day which vessel visits which installation and in what order.

First index is vesse, then day in schedule period. That array contains the
order of which installations are visited, and in which order padded with zeros
at the end. Zero also represents the depot. Only zeros represents the vessel
staying at the depot that day.

In the following example the second vessel (index 1) does not sail on day one,
visits installation 1 on day 2 and visits installation 2, 3 and 4 in that order
on day 7.
```
array([[[0, 0, 0, 0],
        [2, 0, 0, 0],
        [3, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],

       [[1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 0],
        [1, 2, 0, 0],
        [0, 0, 0, 0],
        [2, 3, 4, 0]]], dtype=int8)
```


<!-- [![PyPI - Version](https://img.shields.io/pypi/v/psvpp-solver.svg)](https://pypi.org/project/psvpp-solver) -->
<!-- [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psvpp-solver.svg)](https://pypi.org/project/psvpp-solver) -->

-----

**Table of Contents**

<!-- - [Installation](#installation) -->
- [License](#license)

<!-- ## Installation -->

<!-- ```console -->
<!-- pip install psvpp-solver -->
<!-- ``` -->

## License

`psvpp-solver` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## References
<a id="1">[1]</a> 
Borthen, Thomas, et al. "A genetic search-based heuristic for a fleet size and
periodic routing problem with application to offshore supply planning." EURO
Journal on Transportation and Logistics 7.2 (2018): 121-150.
