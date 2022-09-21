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
def sample(G, n, sample_p):
    P = []
    for node in G.nodes:
        a = random.random()
        if a < sample_p:
            P.append(node)
    return P

def labeling(G, S):
    for node in G.nodes:
        node.a = nx.ancestors(G, node)
        #node.a.append(node)
        #node.aS = list(set(node.a).intersection(S))

        node.d = nx.descendants(G, node)
        #node.d.append(node)
        #node.dS = list(set(node.d).intersection(S))
        node.a = list(nx.ancestors(G, node))
        node.a.append(node)
        node.aS = list(set(node.a).intersection(S))
        for i in range(len(node.a)):
            node.a[i] = node.a[i].data
        node.d = list(nx.descendants(G, node))
        node.d.append(node)
        print(node.d)
        print(set(node.d))
        print(S)
        print(set(node.d).intersection(S))
        node.dS = list(set(node.d).intersection(S))
        for j in range(len(node.d)):
            node.d[j] = node.d[j].data
    return 

def partition(G):
    subgraphs = []
    subgraphs_with_label = []
    # find the node that has the same ancestors and descendants with another node
    queue = [G.nodes]
    for node in queue:
        subgraph = [node]
        subgraph_with_label = [node.data]
        print(node)
        for node2 in queue:
            if node.aS == node2.aS and node.dS == node2.dS:
                subgraph.append(node2)
                subgraph_with_label.append(node2.data)
                queue.remove(node2)
        subgraphs.append(subgraph)
        subgraphs_with_label.append(subgraph_with_label)
        queue.remove(node)
    return subgraphs, subgraphs_with_label
                


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
S = sample(G, n, sample_p)
print(S)
print("--- %s seconds for sampling a graph ---" % (time.time() - start_time))

start_time = time.time()
labeling(G, S)
for node in G.nodes:
    print("Node", node.data,"   Ancestors:", node.a, "   Decendents:", node.d)
    print(node.aS)
    print(node.dS)
print("--- %s seconds for finding ancestors and descendants ---" % (time.time() - start_time))

#subgraphs, subgraphs_with_label= partition(G)
#print("Subgraphs:", subgraphs_with_label)

# Draw graph
labeldict = {}
for node in G.nodes:
    labeldict[node] = node.data
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, labels=labeldict)
plt.title("Random Graph Generation Example")
plt.show()

