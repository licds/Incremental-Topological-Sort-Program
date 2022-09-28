from randomDAGGeneration1 import ER
import math
import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np

# Calculate sample rate based on number of rounds
def sample_rate(power, n):
    sample_p = (math.log(n))**power/n
    return sample_p

# Sampling function, Runtime O(n)
def sample(G, sample_p):
    S = []
    for node in G.nodes:
        a = random.random()
        if a < sample_p:
            S.append(node)
    return S

# Label each node with ancestors, descendants, and intersection with sample S
def labeling(G, S):
    for node in G.nodes:
        node.aS = []
        node.dS = []
    for s in S:
        s.a = list(nx.ancestors(G, s))
        s.a.append(s)
        s.d = list(nx.descendants(G, s))
        s.d.append(s)
        for i in s.a:
            i.dS.append(s)
        for j in s.d:
            j.aS.append(s)
    return 

# Partition graph into subgraphs through labels, S-equivalent will create subgraph
def partition(G):
    subgraphs = []
    queue = []
    # find the node that has the same ancestors and descendants with another node
    for node in G.nodes:
        queue.append(node)
    for node in queue:
        subgraph = []
        for node2 in queue:
            if node.aS == node2.aS and node.dS == node2.dS:
                subgraph.append(node2)
        subgraphs.append(tuple(subgraph))
    subgraphs = set(subgraphs)
    return subgraphs

# Print all information of graph and nodes  
def print_info(S, G, subgraphs):
    print("")
    print("##### Graph Output #####")
    print("Sampled nodes are the following:", end =" ")
    for s in S:
        print(s.data, end =" ")
    print("")
    for node in G.nodes:
        print("Node", node.data)
        print("     Ancestors:", end =" ")
        for ancester in node.a:
            print(ancester.data, end =" ")
        print("")
        print("     Descendants:", end =" ")
        for descendent in node.d:
            print(descendent.data, end =" ")
        print("")
        print("     Ancestors in sample S:", end =" ")   
        if len(node.aS) == 0:
            print("Empty", end =" ") 
        else:
            for ancester in node.aS:
                print(ancester.data, end =" ")
        print("")
        print("     Descendants in sample S:", end =" ")
        if len(node.dS) == 0:
            print("Empty", end =" ") 
        else:
            for descendent in node.dS:
                print(descendent.data, end =" ")
        print("")
    print("The following subgraphs are formed:")
    i = 1
    for subgraph in subgraphs:
        print("Subgraph", i, "contains: ", end =" ")
        i += 1
        for node in subgraph:
            print(node.data, end =" ")
        print("")


