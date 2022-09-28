from DAG1 import ER
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
def sample(nodes, sample_p):
    S = []
    for node in nodes:
        a = random.random()
        if a < sample_p:
            S.append(node)
    return S

# Label each node with ancestors, descendants, and intersection with sample S
def labeling(G, nodes, S):
    for node in nodes:
        node.aS = []
        node.dS = []
    for s in S:
        s.a = list(set(nx.ancestors(G, s)).intersection(set(nodes)))
        s.a.append(s)
        s.d = list(set(nx.descendants(G, s)).intersection(set(nodes)))
        s.d.append(s)
        for i in s.a:
            i.dS.append(s)
        for j in s.d:
            j.aS.append(s)
    return 

# Partition graph into subgraphs through labels, S-equivalent will create subgraph
def partition(nodes):
    subgraphs = []
    queue = []
    # find the node that has the same ancestors and descendants with another node
    for node in nodes:
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

def round(G, nodes, r):
    sample_p = sample_rate(r, len(G.nodes))
    S = sample(nodes, sample_p)
    labeling(G, nodes, S)
    subgraphs = partition(nodes)
    return [subgraphs, S]

def rounds(details, samples, graphs, G, nodes):
    r = 1
    result = round(G, nodes, r)
    adict = {}
    ddict = {}
    for node in G.nodes:
        adict[node] = node.aS
        ddict[node] = node.dS
    details.append([adict, ddict])
    graphs.append(result[0])
    samples.append(result[1])
    wait = []
    for subgraph in graphs[r-1]:
        if len(subgraph) > 1:
            wait.append(subgraph)
    while len(wait) > 0:
        r += 1
        graphs.append([])
        samples.append([])
        for subgraph in wait:
            result = round(G, subgraph, r)
            graphs[r-1].extend(result[0])
            samples[r-1].extend(result[1])
        wait = []
        for subgraph in graphs[r-1]:
            if len(subgraph) > 1:
                wait.append(subgraph)
        adict = {}
        ddict = {}
        for node in G.nodes:
            adict[node] = node.aS
            ddict[node] = node.dS
        details.append([adict, ddict])

def decode_graphs(sets):
    i = 0
    j = 0
    sets_info = []
    for subsets in sets:
        sets_info.append([])
        for subset in subsets:
            sets_info[i].append([])
            for node in subset:
                sets_info[i][j].append(node.data)
            j += 1
        i += 1
        j = 0
    print("##### GRAPH INFO #####")
    for i in sets_info:
        print(i)

def decode_samples(sets):
    samples_info = []
    i = 0
    for sample in sets:
        samples_info.append([])
        for node in sample:
            samples_info[i].append(node.data)
        i += 1
    print("##### SAMPLE INFO #####")
    for i in samples_info:
        print(i)    

def decode_details(details):
    i = 1
    for round in details:
        print("##### Round", i, "#####")
        max = -1
        for node in round[0].keys():
            if len(round[0][node]) > max:
                max = len(round[0][node])
        for node in round[0].keys():
            temp = 0
            print("Node", node.data, "has ancestors     ", end =" ")
            for a in round[0][node]:
                print(a.data, end =" ")
                temp += 1
            print("  "*(max-temp), end="")
            print("        descendents", end="     ")
            for d in round[1][node]:
                print(d.data, end =" ")
            print("")
        i += 1
    
def draw(G):
    labeldict = {}
    for node in G.nodes:
        labeldict[node] = node.data
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, labels=labeldict)
    plt.title("Random Graph Generation Example")
    plt.show()