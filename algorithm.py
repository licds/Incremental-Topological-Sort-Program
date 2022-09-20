import math
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import itertools
import numpy as np
from randomDAGGeneration import ER

# Accelerate runtime through taichi
#ti.init(arch=ti.gpu)

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
    #N = dict()
    for node in P:
        A[node] = nx.ancestors(G, node)
        D[node] = nx.descendants(G, node)
        #N[node] = set(G.nodes) - (A[node] | D[node])
    return A, D

# Number of nodes and probability for edges, INPUT HERE #################################
n = 10
p = 0.2

# Probability for partition
partition_p = math.log(n)/n


# Calculate size of m based on p
m = math.ceil(math.log(0.000000001,10)/math.log(1-p,10)-1)

# ER is relatively fast but still pretty bad especially after 10,000
start_time = time.time()
G = ER(n, p)
print("--- %s seconds for generating a graph using ER ---" % (time.time() - start_time))

start_time = time.time()
P = partition(n, partition_p)
print("--- %s seconds for partitioning a graph ---" % (time.time() - start_time))

start_time = time.time()
A, D = labeling(G, P)
print("--- %s seconds for finding ancestors and descendants ---" % (time.time() - start_time))

# Draw graph
#pos = nx.spring_layout(G)
#nx.draw_networkx(G, pos)
#plt.title("Random Graph Generation Example")
#plt.show()

