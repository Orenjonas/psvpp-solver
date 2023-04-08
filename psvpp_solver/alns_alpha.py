import numpy as np

# Adaptive Large Neighbourhood Search for the Periodic Supply Vessel Planning Problem (PSVPP)


# 1: State Set the cost of the best known solution
cost_best_known = np.Inf
g_best = []

# 2: for n restarts do

n_restarts = 10

for i in range(n_restarts):
    # 3: Construct initial solution g0 satisfying reliability constraint
    # 4: g g g g ; ; ( ); 1 / g µ 0 0 0 ;
    # 5: for iterations do
    # 6: g ( , , ) g q S , remove q visits;
    # 7: g ( , , ) g q S
    # , insert q visits while satisfying (4);
    # 8: if S = and g is feasible then
    # 9: while g improves do
    # 10: Run the set of improvement operators while satisfying (4);
    # 11: end while
    # 12: if
    # ( ) ( ) g g then
    # 13: g g g g ; ;
    # 14: else if
    # ( ) ( ) g g then
    # 15: g g ;
    # 16: else
    # 17: g g with probability e ( ( ) ( ))/ g g ;
    # 18: end if
    # 19: end if
    # 20: µ ;
    # 21: end for
    # 22: end for
    # 23: return g
    pass
