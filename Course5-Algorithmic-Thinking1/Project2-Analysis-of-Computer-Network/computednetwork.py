from pylab import *
import matplotlib.pyplot as plt
import numpy as np

"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
from collections import deque

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def make_random_undirected_graph(num_nodes, p):
    graph = {}
    if num_nodes < 1:
        return graph
    for node in range(num_nodes):
        graph[node] = set([])
    for node in range(num_nodes):
        for dummy_i in range(num_nodes):
            if dummy_i != node:
                a = random.random()
                if a < p:
                    graph[node].add(dummy_i)
                    graph[dummy_i].add(node)
    return graph
    


"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes and returns a dictionary
    corresponding to a complete directed graph.
    """
    graph = {}
    for node in range(num_nodes):
        graph[node] = set(range(num_nodes))
        graph[node].remove(node)
    return graph    
    
    
def make_upa_graph (total_nodes, m):
    graph = make_complete_graph(m)
    trial = UPATrial(m)
    for node in range(m, total_nodes):
        new_node_neighbors = trial.run_trial(m)
        graph[node] = new_node_neighbors
        for neighbor in new_node_neighbors:
            graph[neighbor].add(node)	
    return graph

#dpa_obj = UPATrial(5)
#print dpa_obj._node_numbers
#dpa_obj.run_trial(5)
#print dpa_obj._node_numbers

#print load_graph(NETWORK_URL)

#g1 = make_random_undirected_graph(10, 0.2)
#print g1
g2 = make_upa_graph(6, 5)
print g2

def random_order(graph):
    result = []
    for node in graph:
        result.append(node)
    shuffle(result)
    return result

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node
    and returns the set consisting of all nodes that are 
    visited by a breadth-first search that starts at start_node.
    """
    bfs_queue = deque()
    visited = set([])
    visited.add(start_node)
    bfs_queue.append(start_node)
    while len(bfs_queue) != 0:
        node_j = bfs_queue.pop()
        neighbors = ugraph[node_j]
        for nbr in neighbors:
            if nbr not in visited:
                visited.add(nbr)
                bfs_queue.append(nbr)
    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of 
    sets, where each set consists of all the nodes (and 
    nothing else) in a connected component, and there 
    is exactly one set in the list for each connected 
    component in ugraph and nothing else.
    """
    remaining_nodes = ugraph.keys()
    connected_comp_list = []
    while len(remaining_nodes) != 0:
        working_set = bfs_visited(ugraph, remaining_nodes[0])
        connected_comp_list.append(working_set)
        for node in working_set:
            remaining_nodes.remove(node)
    return connected_comp_list
        
def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size
    (an integer) of the largest connected component in 
    ugraph.
    """
    largest = 0;
    connected_comp_list = cc_visited(ugraph)
    for connected_comp in connected_comp_list:
        size = len(connected_comp)
        if size > largest:
            largest = size
    return largest
    
def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes 
    attack_order and iterates through the nodes in 
    attack_order. 
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    resilience_list = []
    size = largest_cc_size(new_graph)
    resilience_list.append(size)
    for attacked_node in attack_order:
        new_graph.pop(attacked_node)
        for dummy_node in new_graph:
            if attacked_node in new_graph[dummy_node]:
                new_graph[dummy_node].remove(attacked_node)
        size = largest_cc_size(new_graph)
        resilience_list.append(size)
    return resilience_list


N = 1347
E = 3112
PROBABILITY = 0.003433
M = 5

computer_network_graph = load_graph(NETWORK_URL)
ER_graph = make_random_undirected_graph(N, PROBABILITY)
UPA_graph = make_upa_graph(N, M)

network_resilience = compute_resilience(computer_network_graph, random_order(computer_network_graph))
ER_resilience = compute_resilience(ER_graph, random_order(ER_graph))
UPA_resilience = compute_resilience(UPA_graph, random_order(UPA_graph))


plt.plot(network_resilience, 'b-', label='computer network')
plt.plot(ER_resilience, 'r-', label='ER graph, p=0.003433')
plt.plot(UPA_resilience, 'g-', label='UPA graph, m=5')
plt.legend(loc='upper right')

title('Resilience of networks under a random attack');
plt.xlabel('Number of nodes removed')
plt.ylabel('Size of the largest connected component')
plt.show()

## Q3.

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    

def fast_targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    new_graph = copy_graph(ugraph)  
    degree_sets = []
    order = []
    n = len(new_graph)
    degree_sets = [set() for _ in xrange(n)]
    for node in new_graph:
        node_deg = len(new_graph[node])
        degree_sets[node_deg].add(node)
        
    for degree in range(n-1, -1, -1):
        while len(degree_sets[degree]) != 0:
            max_degree_node = degree_sets[degree].pop()
            neighbors = new_graph[max_degree_node]
            for neighbor in neighbors:
                neighbor_degree = len(new_graph[neighbor])
                degree_sets[neighbor_degree].discard(neighbor)
                degree_sets[neighbor_degree-1].add(neighbor)
                new_graph[neighbor].remove(max_degree_node)
            order.append(max_degree_node)
            new_graph.pop(max_degree_node)
    return order

#print "WANT", targeted_order(computer_network_graph)

#print "COMPUTER GRAPH", computer_network_graph
#print "FAST", fast_targeted_order(computer_network_graph)    


def running_time_best():
    running_times_norm = []
    running_times_fast = []
    for n in range (10, 1000, 10):
        upa_graph = make_upa_graph(n, 5)
        start = time.clock()
        targeted_order(upa_graph)   
        stop = time.clock()
        elapsed_time = stop - start
        running_times_norm.append(elapsed_time)
        start = time.clock()
        fast_targeted_order(upa_graph)   
        stop = time.clock()
        elapsed_time = stop - start
        running_times_fast.append(elapsed_time)
    
    #print "norm", running_times_norm
    #print "fast", running_times_fast
    return running_times_norm, running_times_fast

time_norm, time_fast = running_time_best()

#print "running time norm", time_norm
#print "running time fast", time_fast

x = np.arange(10, 1000, 10)
plt.plot(x, time_norm, 'b-', label='targeted_order')
plt.plot(x, time_fast, 'r-', label='fast_targeted_order')

plt.legend(loc='upper right')

title('Order of Growth of Target Functions using Desktop Python');
plt.xlabel('Number of nodes')
plt.ylabel('Running Time')
plt.show()

network_resilience_targeted = compute_resilience(computer_network_graph, targeted_order(computer_network_graph))
ER_resilience_targeted = compute_resilience(ER_graph, targeted_order(ER_graph))
UPA_resilience_targeted = compute_resilience(UPA_graph, targeted_order(UPA_graph))

plt.plot(network_resilience_targeted, 'b-', label='computer network')
plt.plot(ER_resilience_targeted, 'r-', label='ER graph, p=0.003433')
plt.plot(UPA_resilience_targeted, 'g-', label='UPA graph, m=5')
plt.legend(loc='upper right')

title('Resilience of networks under a targeted attack');
plt.xlabel('Number of nodes removed')
plt.ylabel('Size of the largest connected component')
plt.show()