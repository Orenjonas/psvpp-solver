def visualize_route(routes,
                    visits,
                    n_days=4):
    """
    Plot graph of tours for each vessel for each day in genome
    """
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt

    n_vessels = len(routes)
    n_installations = len(visits)

    fig, ax = plt.subplots(n_vessels, n_days)

    for day in range(n_days):
        for vessel in range(n_vessels):
            # Just one day
            G = nx.DiGraph()
            nodes = np.arange(0, n_installations + 1).tolist()
            G.add_nodes_from(nodes)

            day_routes = routes[vessel][day]

            # Add departure from base
            if (len(day_routes) > 0):
                out = []
                out.append((0, day_routes[0]))

                for i in range(1, len(day_routes)):
                    out.append((day_routes[i-1], day_routes[i]))

                # Add return to base
                out.append((out[-1][-1], 0))

                G.add_edges_from(out)

            pos = {0: (1, 0)}

            # Position of installations - spread positions upwards from base
            for i in range(1, len(visits) + 1):
                pos[i] = (0.5 + i % 2 + i*0.1,
                          1 + np.floor(i / 2))

            nx.draw_networkx(G,
                             pos=pos,
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
    visualize_route(parent_1)
