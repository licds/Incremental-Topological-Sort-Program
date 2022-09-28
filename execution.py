import math
import matplotlib.pyplot as plt
import networkx as nx
import time
import numpy as np
import taichi as ti
from randomDAGGeneration import ER
from algorithm import *

# Accelerate runtime through taichi
ti.init(arch=ti.gpu)

################################# Number of nodes and probability for edges, INPUT HERE #################################
<<<<<<< HEAD:execution.py
<<<<<<< HEAD:execution.py
n = 100
=======
n = 10
>>>>>>> parent of 910000d (Labeling fixed):execution1.py
=======
n = 10
>>>>>>> parent of 910000d (Labeling fixed):execution1.py
p = 0.2

################################# Probability for sampling #################################
sample_p = sample_rate(1, n)


# Calculate size of m based on p
# m = math.ceil(math.log(0.000000001,10)/math.log(1-p,10)-1)

print("##### RUNTIME ANALYSIS #####")
# Generate a random graph with ER
start_time = time.time()
G = ER(n, p)
print("--- %s seconds for generating a graph using ER ---" % (time.time() - start_time))

# Sample nodes
start_time = time.time()
S = sample(G, sample_p)
print("--- %s seconds for sampling a graph ---" % (time.time() - start_time))

# Label every nodes with ancestors and descendants, as well as intersection with sample S
start_time = time.time()
labeling(G, S)
print("--- %s seconds for labeling each node ---" % (time.time() - start_time))

start_time = time.time()
subgraphs = partition(G)
print("--- %s seconds for breaking graph into subgraphs ---" % (time.time() - start_time))

print_info(S, G, subgraphs)

# Draw graph

labeldict = {}
for node in G.nodes:
    labeldict[node] = node.data
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, labels=labeldict)
plt.title("Random Graph Generation Example")
<<<<<<< HEAD:execution.py
plt.show()
<<<<<<< HEAD:execution.py
=======
plt.show()
>>>>>>> parent of 910000d (Labeling fixed):execution1.py
=======
>>>>>>> parent of 910000d (Labeling fixed):execution1.py
