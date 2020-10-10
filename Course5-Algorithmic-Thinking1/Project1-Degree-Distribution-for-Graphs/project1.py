"""Compute indegree of a graph and degree distibution."""

'''
    Define three constants whose values are dictionaries
    corresponding to the three directed graphs shown in these
    linked diagrams: EX_GRAPH0, EX_GRAPH1, and EX_GRAPH2. Note
    that the label for each node in the diagrams should be
    represented as an integer. You should use these graphs in
    testing your functions that compute degree distributions.
    http://storage.googleapis.com/codeskulptor-alg/alg_example_graph0.jpg
    http://storage.googleapis.com/codeskulptor-alg/alg_example_graph1.jpg
    http://storage.googleapis.com/codeskulptor-alg/alg_example_graph2.jpg
    '''


EX_GRAPH0 = {
    0: set([1, 2]),
    1: set(),
    2: set()
}

EX_GRAPH1 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3]),
    3: set([0]),
    4: set([1]),
    5: set([2]),
    6: set()
}

EX_GRAPH2 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3, 7]),
    3: set([7]),
    4: set([1]),
    5: set([2]),
    6: set(),
    7: set([3]),
    8: set([1, 2]),
    9: set([0, 3, 4, 5, 6, 7])
}


def make_complete_graph(num_nodes):
    """Make graph where each node is connected to all other nodes"""
    def all_but(num_n, num_i):
        """Make a list of all numbers upto n excluding ith"""
        return [num_x for num_x in range(num_n) if num_x != num_i]

    return {num_i: set(all_but(num_nodes, num_i))
            for num_i in range(num_nodes)}


def compute_in_degrees(digraph):
    """Compute how many nodes enter current node"""
    degrees = {key: 0 for key in digraph.keys()}
    for _, adjacent in digraph.items():
        for adj in adjacent:
            degrees[adj] += 1
    return degrees


def in_degree_distribution(digraph):
    """How many different indegrees we have in the graph"""
    num_n = len(digraph.keys())
    num_nlarge = num_n * (num_n - 1) / 2
    distr = {}
    in_degrees = compute_in_degrees(digraph)
    for _, indegree in in_degrees.items():
        if indegree in distr:
            distr[indegree] += 1
        else:
            distr[indegree] = 1
    return {key: value for key, value in distr.items() if value > 0}


# Testing
print make_complete_graph(3)
#print make_complete_graph(5)
#print make_complete_graph(0)
#print make_complete_graph(-3)
#print compute_in_degrees(EX_GRAPH0)
#print compute_in_degrees(EX_GRAPH1)
#print compute_in_degrees(EX_GRAPH2)
#print in_degree_distribution(EX_GRAPH2)
