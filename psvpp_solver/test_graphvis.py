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
