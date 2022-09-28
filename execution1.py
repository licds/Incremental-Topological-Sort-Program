from cmath import log
import math
import matplotlib.pyplot as plt
import networkx as nx
import time
import numpy as np
import taichi as ti
from DAG1 import ER
from algorithm1 import *

# Accelerate runtime through taichi
ti.init(arch=ti.gpu)

################################# Number of nodes and probability for edges, INPUT HERE #################################
n = 10
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
S = sample(G.nodes, sample_p)
print("--- %s seconds for sampling a graph ---" % (time.time() - start_time))

# Label every nodes with ancestors and descendants, as well as intersection with sample S
start_time = time.time()
labeling(G, G.nodes, S)
print("--- %s seconds for labeling each node ---" % (time.time() - start_time))

start_time = time.time()
subgraphs = partition(G.nodes)
print("--- %s seconds for breaking graph into subgraphs ---" % (time.time() - start_time))

# print_info(S, G, subgraphs)
start_time = time.time()
details = []
graphs = []
samples = []
rounds(details, samples, graphs, G, G.nodes)
print("--- %s seconds for doing rounds ---" % (time.time() - start_time))

graphs_info = decode_graphs(graphs)
samples_info = decode_samples(samples)


print("##### GRAPH INFO #####")
for i in graphs_info:
    print(i)

print("##### SAMPLE INFO #####")
for i in samples_info:
    print(i)

i = 1
for round in details:
    print("##### Round", i, "#####")
    for adict in round:
        for node in adict.keys():
            print("Node", node.data, "has ancestors", end =" ")
            for a in adict[node]:
                print(a.data, " ", end =" ")
            print("")
    for ddict in round:
        for node in adict.keys():
            print("Node ", node.data, "has descendents", end =" ")
            for d in ddict[node]:
                print(d.data, end =" ")
            print("")
    i += 1

#draw(G)