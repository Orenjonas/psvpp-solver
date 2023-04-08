def visualize_route(genome, n_days=4):
    """
    Plot graph of tours for each vessel for each day in genome
    """
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt

    n_vessels = len(genome[2])

    fig, ax = plt.subplots(n_vessels, n_days)

    for day in range(n_days):
        for vessel in range(n_vessels):
            # print('day: ', day, ' vessel: ', vessel)
            # Just one day
            G = nx.DiGraph()
            nodes = np.arange(0, len(genome[1])).tolist()
            G.add_nodes_from(nodes)

            day_routes = genome[0][vessel][day]
            # print("day_routes", day_routes)

            # Add departure from base
            # from IPython import embed
            # embed()
            if (len(day_routes) > 0):
                out = []
                out.append((0, day_routes[0]))

                for i in range(1, len(day_routes)):
                    # print("out", out, "\ni:", i)
                    out.append((day_routes[i-1], day_routes[i]))

                # Add return to base
                out.append((out[-1][-1], 0))

                G.add_edges_from(out)

            pos = {0: (1, 0)}

            # Position of installations
            for i in range(1, len(genome[1]) + 1):
                pos[i] = (0.5 + i % 2 + i*0.1,
                          1 + np.floor(i / 2))

            # pos = {0: (7, 6),
            #        1: (4, 7), 2: (6, 7), 3: (8, 7),
            #        4: (5, 8), 5: (7, 8), 6: (9, 8),
            #        7: (4.5, 9)}
            # labels = {0: "CEO",
            #           1: "Team A Lead", 2: "Team B Lead",
            #           3: "Staff A", 4: "Staff B",
            #           5: "Staff C", 6: "Staff D", 7: "Staff E"}
            nx.draw_networkx(G,
                             pos=pos,
                             # labels=labels,
                             arrows=True,
                             node_shape="s",
                             node_color="white",
                             ax=ax[vessel, day])

            ax[vessel, day].set_title(
                "PVS: "+str(vessel) + " Day: " + str(day))
# plt.savefig("Output/plain organogram using networkx.jpeg",
#             dpi=300)
    plt.show()


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
        # tour [PSV][day]
        [[[1, 2, 4], [],     [4, 3, 2], []],
         [[],     [3, 4], [],        [1, 2]]
         ],
        # installations [instsallation][day visited]
        [[1, 4], [1, 3, 4], [2, 3], [2, 3]],
        # vessels [vessel][day departing]
        [[1, 3], [2, 4]]
    ]
    visualize_route(parent_2)
