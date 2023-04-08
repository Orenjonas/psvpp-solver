def visualize_route(route):
    import numpy as np
    from graphviz import Graph

    # Instantiate a new Graph object
    dot = Graph('Data Science Process', format='png')

    # Add nodes
    for i in range(5):
        dot.node(str(i), str(i))

    # dot.node('A', 'Get Data')
    # dot.node('B', 'Clean, Prepare, & Manipulate Data')
    # dot.node('C', 'Train Model')
    # dot.node('D', 'Test Data')
    # dot.node('E', 'Improve')

    # Connect these nodes
    dot.edges(['01', '12', '20', '03', '34', '40'])

    # Save chart
    dot.render('data_science_flowchart', view=True)


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
    visualize_route(parent_2)
