import matplotlib.pyplot as plt
import networkx as nx
import math
import time
from itertools import combinations
from random import random
import taichi as ti

ti.init(arch=ti.gpu)

# Following function from https://compucademy.net/generating-random-graphs-in-python/
# Runtime O(n^2)
def ER(n, p):
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        a = random()
        if a < p:
            E.add(combination)

    g = nx.DiGraph() # Create directed graph
    g.add_nodes_from(V)
    g.add_edges_from(E)

    return g

# Runtime O(n)
def partition(n, partition_p):
    P = []
    for node in range(n):
        a = random()
        if a < partition_p:
            P.append(node)
    return P

# Number of nodes and probability for edges
n = 20000
p = 0.2

# Probability for partition
partition_p = math.log(n)/n

# Generate random graph and partition
start_time = time.time()
G = ER(n, p)
print("--- %s seconds for generating a graph ---" % (time.time() - start_time))
start_time = time.time()
P = partition(n, partition_p)
print("--- %s seconds for partitioning a graph ---" % (time.time() - start_time))
start_time = time.time()
A = dict()
D = dict()
for node in P:
    A[node] = nx.ancestors(G, node)
    D[node] = nx.descendants(G, node)
print("--- %s seconds for finding ancestors and descendants ---" % (time.time() - start_time))




# Draw graph
"""
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
plt.title("Random Graph Generation Example")
plt.show()
"""
# 