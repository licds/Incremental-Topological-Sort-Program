from randomDAGGeneration import ER
import math
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import numpy as np


# Accelerate runtime through taichi
#ti.init(arch=ti.gpu)

# Sampling function, Runtime O(n)
def sample(n, sample_p):
    P = []
    for node in range(n):
        a = random.random()
        if a < sample_p:
            P.append(node)
    return P

def labeling(G):
    for node in G.nodes:
        node.a = list(nx.ancestors(G, node))
        node.a.append(node)
        for i in range(len(node.a)):
            node.a[i] = node.a[i].data
        node.d = list(nx.descendants(G, node))
        node.d.append(node)
        for j in range(len(node.d)):
            node.d[j] = node.d[j].data
    return 

def partition(S, G):
    for node in G.nodes:
        if P 

# Number of nodes and probability for edges, INPUT HERE #################################
n = 10
p = 0.2

# Probability for sampling
sample_p = math.log(n)/n


# Calculate size of m based on p
m = math.ceil(math.log(0.000000001,10)/math.log(1-p,10)-1)

# ER is relatively fast but still pretty bad especially after 10,000
start_time = time.time()
G = ER(n, p)
print("--- %s seconds for generating a graph using ER ---" % (time.time() - start_time))

start_time = time.time()
P = sample(n, sample_p)
print("--- %s seconds for sampling a graph ---" % (time.time() - start_time))

start_time = time.time()
labeling(G)
for node in G.nodes:
    print("Node", node.data,"   Ancestors:", node.a, "   Decendents:", node.d)
print("--- %s seconds for finding ancestors and descendants ---" % (time.time() - start_time))

print(G)
# Draw graph
labeldict = {}
for node in G.nodes:
    labeldict[node] = node.data
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, labels=labeldict)
plt.title("Random Graph Generation Example")
plt.show()

