import math
import random
import time
import pandas as pd
import pickle
import numpy as np

def sample_rate(power, n):
    sample_p = (math.log(n))**power/n
    return sample_p

# Approach 2 ######## BETTER ########
def sample(nodes, sample_p):
    S = set()
    for node in nodes:
        a = random.random()
        if a < sample_p:
            S.add(node)
    return S

def newsample(nodes):
    samples_round = {}
    r = 1
    n = len(nodes)
    while len(nodes) != 0:
        S = sample(nodes, sample_rate(r, n))
        samples_round[r] = S
        nodes = nodes-S
        r += 1
    return samples_round

def labeldict(nodes, edges):
    adict = {}
    ddict = {}
    for edge in edges:
        if edge[0] in adict:
            adict[edge[0]].append(edge[1])
        else:
            adict[edge[0]] = [edge[1]]
        if edge[1] in ddict:
            ddict[edge[1]].append(edge[0])
        else:
            ddict[edge[1]] = [edge[0]]
    for node in nodes:
        if node not in adict:
            adict[node] = []
        if node not in ddict:
            ddict[node] = []
    return adict, ddict

def labeling(nodes, samples, r, adict, ddict):
    ancestors = {}
    descendants = {}
    unique = set(nodes)
    samples = list(unique.intersection(set(samples[r])))
    for node in nodes:
        ancestors[node] = []
        descendants[node] = []
    for s in samples:
        notvisit_ans = list(set(adict[s].copy()).intersection(unique))
        notvisit_des = list(set(ddict[s].copy()).intersection(unique))
        ancestors[s].append(s)
        descendants[s].append(s)
        while len(notvisit_ans) > 0:
            node = notvisit_ans.pop(0)
            ancestors[node].append(s)
            notvisit_ans.extend(list(set(adict[node]).intersection(unique)))
        while len(notvisit_des) > 0:
            node = notvisit_des.pop(0)
            descendants[node].append(s)
            notvisit_des.extend(list(set(ddict[node]).intersection(unique)))
    return ancestors, descendants

def label(ancestors, descendants):
    keys = ancestors.keys()
    values = zip(ancestors.values(), descendants.values())
    combined = dict(zip(keys, values))
    return combined

def partition_df(combined):
    df = pd.DataFrame({'key':combined.keys(), 'value':combined.values()})
    subgraphs = []
    for val in list(map(pickle.loads, dict.fromkeys(map(pickle.dumps, list(df.value))))):
        subgraph = list(df.key[df.value==val])
        if len(subgraph) > 1:
            subgraphs.append(subgraph)
    return subgraphs

def partition(combined):
    vals = np.array(list(combined.items()), dtype=object)
    uniq, count = np.unique(vals[:,1], return_counts=True)
    uniq = uniq[count > 1]
    subgraphs = []
    for val in uniq:
        subgraph = []
        for row in range(len(vals)):
            if vals[row,1] == val:
                subgraph.append(vals[row,0])
        subgraphs.append(subgraph)
    return subgraphs

def graph(types, n):
    nodes = []
    edges = []
    if types == 'line':
        nodes = set(range(n))
        edges = []
        for i in range(n-1):
            edges.append((i, i+1))       
        return nodes, edges
    elif types == 'perfect':
        layers = []
        nodes = set(range(1,n+1))
        x = 1
        y = 2
        while x+y < n:
            layers.append(list(range(x, n+1, y)))
            x = x*2
            y = y*2
        layers.append(list(range(x, n+1, y)))
        for i in range(1,len(layers)):
            for j in range(len(layers[i])):
                try:
                    edges.append((layers[i][j], layers[i-1][j*2]))
                except:
                    pass
                try:
                    edges.append((layers[i][j], layers[i-1][j*2+1]))
                except:
                    pass
        return nodes, edges


##### Takes 0.13-0.14s for sampling 100000 nodes
# sample_time = 0
# for i in range(100):
#     nodes = set(range(100000))
#     start = time.time()
#     newsample(nodes)
#     end = time.time()
#     sample_time += end-start
# print("sample_time:", sample_time/100)

##### Takes 1.4-1.5s for labeling 100000 nodes
# label_time = 0
# for i in range(10):
#     samples_round = newsample(nodes)
#     start = time.time()
#     adict, ddict = labeldict(edges)
#     ancestors, descendants = labeling(nodes, samples_round, 1,adict, ddict)
#     end = time.time()
#     label_time += end-start
# print("label_time:", label_time/10)

# nodes = set([0, 1, 2, 3, 4, 5, 6, 7])
# edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
# samples_round = {}

# samples_round[1] = [2, 3, 6]
# samples_round[2] = [1, 4, 5]
# adict, ddict = labeldict(nodes, edges)

#### Graph Initialization ####
n = 16 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
nodes, edges = graph('line', n) #line, perfect
adict, ddict = labeldict(nodes, edges)

begin = time.time()
i = 1
subgraphs = [nodes]
start = time.time()
samples_round = newsample(nodes)
print("sample :", samples_round)
sample_time = time.time()-start
label_time = 0
partition_time = 0
while len(subgraphs) > 0:
    print("Round", i, ":", subgraphs)
    ancestors = {}
    descendants = {}
    graphs = []
    for subgraph in subgraphs:
        start = time.time()
        anc, des = labeling(subgraph, samples_round, i, adict, ddict)
        combined = label(anc, des)
        label_time += time.time()-start
        start = time.time()
        graph = partition(combined)
        graphs.extend(graph)
        partition_time += time.time()-start
        start = time.time()
        ancestors.update(anc)
        descendants.update(des)
        label_time += time.time()-start
    start = time.time()
    combined = label(ancestors, descendants)
    label_time += time.time()-start
    print("labels :", combined)
    start = time.time()
    subgraphs = graphs
    partition_time += time.time()-start
    i += 1
end = time.time()
print("sample_time:", sample_time)
print("label_time:", label_time)
print("partition_time:", partition_time)
print("total_time:", end-begin)
# 1. add non-sample node to subgraph
# 2. Save graph to txt file
# 3. Improve partition function using hash sorting