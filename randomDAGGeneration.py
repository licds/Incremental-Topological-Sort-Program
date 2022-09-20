# Following function from https://compucademy.net/generating-random-graphs-in-python/
# Runtime O(n^2)
def ER(n, p):
    """ER
    n: number of vertices
    p: inclusion probability
    """
    V = set([v for v in range(n)])
    
    # Create a list of E possible edges
    E = set()
    for combination in itertools.combinations(V, 2):
        a = random.random()
        if a < p:
            E.add(combination)
    
    # Create directed graph
    G = nx.DiGraph()
    G.add_nodes_from(V)
    G.add_edges_from(E)
    return G
import math
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import itertools
import numpy as np

# Following functio from Pseudo-code https://openproceedings.org/2011/conf/edbt/NobariLKB11.pdf
# Runtime O(n^2)
def PreZER(n, p, m):
    """PreZER
    V: number of vertices
    p: inclusion probability
    m:  number of pre-computations
    """
    # Initiate an empty graph with V nodes
    G = nx.empty_graph(n,create_using=nx.DiGraph())

    # Create a list of E possible edges
    E = numpy_combinations(np.arange(n))

    # Compute the cumulative probability F(i);
    F = []
    for i in range(m+1):
        F.append(1 - pow(1-p,i+1))

    i = -1
    k = -1
    while i < len(E):
        a = random.random()
        # Find the first x where F[x] > a, otherwise use formula; k is # of edges skiped between two selected
        k = next((F.index(x) for x in F if x > a), math.floor(math.log(1-a,1-p)-1))
        i = i+k+1

        # Ignore the last edge
        if i >= len(E):
            break

        # Insert every edge
        G.add_edge(E[i][0], E[i][1])
    return G

# Not complete
def PPreZER(E, p, m, lambda_):
    """PPreZER
    E: maximum number of edges
    p: inclusion probability
    m:  number of pre-computations;
    lambda_: parameter of the block size
    """
    # Initiate an empty graph
    G=nx.empty_graph(0,create_using=nx.DiGraph())

    # Compute the cumulative probability F(i);
    F = []
    for i in range(m+1):
        F[i] = 1 - pow(1-p, i+1)
    
    L = 0
    sigma = math.sqrt(p*(1-p)*E)
    B = p*E + lambda_*sigma
    while L < E:
        R = []
        for i in range(B):
            R.append(random.random())
        S = []

    return 0

# Helper functions
def numpy_combinations(x):
    idx = np.stack(np.triu_indices(len(x), k=1), axis=-1)
    return x[idx]