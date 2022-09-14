import math
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import itertools
import numpy as np
import taichi as ti

# Accelerate runtime through taichi
ti.init(arch=ti.gpu)

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

# Partitioning function, Runtime O(n)
def partition(n, partition_p):
    P = []
    for node in range(n):
        a = random.random()
        if a < partition_p:
            P.append(node)
    return P

def labeling(G, P):
    A = dict()
    D = dict()
    N = dict()
    for node in P:
        A[node] = nx.ancestors(G, node)
        D[node] = nx.descendants(G, node)
        N[node] = set(G.nodes) - (A[node] | D[node])
    return A, D, N

# Helper functions
def numpy_combinations(x):
    idx = np.stack(np.triu_indices(len(x), k=1), axis=-1)
    return x[idx]

# Number of nodes and probability for edges, INPUT HERE #################################
n = 10000
p = 0.2

# Probability for partition
partition_p = math.log(n)/n


# Calculate size of m based on p
m = math.ceil(math.log(0.000000001,10)/math.log(1-p,10)-1)

# Time analysis of two Algorithms, ER is faster but still pretty bad especially after 10,000
#start_time = time.time()
#G= PreZER(n, p, m)
#print("--- %s seconds for generating a graph ---" % (time.time() - start_time))

# Take ER here as one round
start_time = time.time()
G = ER(n, p)
print("--- %s seconds for generating a graph using ER ---" % (time.time() - start_time))

start_time = time.time()
P = partition(n, partition_p)
print("--- %s seconds for partitioning a graph ---" % (time.time() - start_time))

start_time = time.time()
A, D, N = labeling(G, P)
print("--- %s seconds for finding ancestors and descendants ---" % (time.time() - start_time))

# Draw graph
"""
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
plt.title("Random Graph Generation Example")
plt.show()
"""
