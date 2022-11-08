import math
import random
import time
import pickle
from collections import defaultdict

from sklearn.semi_supervised import LabelSpreading

def sample_rate(power, n):
    sample_p = (math.log(n))**power/n
    return sample_p

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

def labeldict(edges):
    adict = defaultdict(set)
    ddict = defaultdict(set)
    for edge in edges:
        adict[edge[0]].add(edge[1])
        ddict[edge[1]].add(edge[0])
    return adict, ddict

def labeling(nodes, samples, r, adict, ddict):
    ancestors = {}
    descendants = {}
    tempdict = {}
    # O(V)
    for node in nodes:
        ancestors[node] = []
        descendants[node] = []
        tempdict[node] = (adict[node].intersection(nodes), ddict[node].intersection(nodes))
    samples = nodes.intersection(samples[r])
    for s in samples:
        notvisit_ans = tempdict[s][0].copy()
        notvisit_des = tempdict[s][1].copy()
        ancestors[s].append(s)
        descendants[s].append(s)
        while len(notvisit_ans) > 0:
            node = notvisit_ans.pop()
            ancestors[node].append(s)
            notvisit_ans.update(tempdict[node][0])
        while len(notvisit_des) > 0:
            node = notvisit_des.pop()
            descendants[node].append(s)
            notvisit_des.update(tempdict[node][1])
    return ancestors, descendants

def label(ancestors, descendants, samples):
    keys = set(ancestors.keys()) - samples
    combined = {}
    for key in keys:
        combined[key] = (tuple(ancestors[key]), tuple(descendants[key]))
    return combined

def partition(combined):
    part_dict = defaultdict(set)
    parts = list(combined.items())
    for part in parts:
        part_dict[part[1]].add(part[0])
    subgraphs = [set(part) for part in part_dict.values()]
    return subgraphs

def graph(types, n):
    if types == 'line':
        nodes = set(range(n))
        edges = []
        for i in range(n-1):
            edges.append((i, i+1))       
        return nodes, edges
    elif types == 'perfect':
        layers = []
        edges = []
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

def test(nodes, adict, ddict, out, samples_round, trials, labels_round):
    label_time = 0
    partition_time = 0 
    total_time = 0
    for i in range(trials):
        begin = time.time()
        i = 1
        subgraphs = [nodes]
        while len(subgraphs) > 0:
            if out == True:
                print("Round", i, ":", subgraphs)
            ancestors = {}
            descendants = {}
            graphs = []
            for subgraph in subgraphs:
                start = time.time()
                anc, des = labeling(subgraph, samples_round, i, adict, ddict)
                label_time += time.time()-start
                start = time.time()
                combined = label(anc, des, samples_round[i])
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
            combined = label(ancestors, descendants, samples_round[i-1])
            label_time += time.time()-start
            if out == True:
                print("labels :", combined)
            labels_round[i] = combined
            start = time.time()
            subgraphs = graphs
            partition_time += time.time()-start
            i += 1
        total_time += time.time()-begin
    print("label_time:", label_time/trials)
    print("partition_time:", partition_time/trials)
    print("total_time:", total_time/trials)

#### Testing Block ####
# n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# # nodes, edges = graph('line', n) #line, perfect
# nodes = set(range(n))
# edges = [(0,1),(1,2),(2,3),(4,5),(5,6),(6,7)]
# labels_round = {}
# # with open('perfect_graph.txt', 'w') as f:
# #     f.write(str(nodes))
# #     f.write('\n')
# #     f.write(str(edges))
# # with open('line_graph100000.txt') as f:
# #     nodes_line = f.readline()
# #     nodes = eval(nodes_line)
# #     edges_line = f.readline()
# #     edges = eval(edges_line)

# adict, ddict = labeldict(edges)
# samples_round = newsample(nodes)
# samples_round[0] = set()
# samples_round[1] = set([0, 7])
# samples_round[2] = set([1,4,5,6])
# samples_round[3] = set([2,3])
# print("sample :", samples_round)
# test(adict, ddict, True, samples_round, 1, labels_round)
# # print("labels_round :", labels_round)
# print("#################################################")

# n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# nodes, edges = graph('line', n) #line, perfect
# adict, ddict = labeldict(edges)
# samples_round = newsample(nodes)
# samples_round[0] = set()
# samples_round[1] = set([0, 7])
# samples_round[2] = set([1,4,5,6])
# samples_round[3] = set([2,3])

# print("sample :", samples_round)
# test(adict, ddict, True, samples_round, 1, labels_round)
# # print("labels_round :", labels_round)






