import math
import random
import time
from tkinter import N

def sample_rate(power, n):
    sample_p = (math.log(n))**power/n
    return sample_p

# Approach 1
def sample1(nodes):
    r = 1
    samples_round = {}
    notvisited = nodes.copy()
    while len(notvisited) != 0:
        samples_round[r] = []
        sample_p = sample_rate(r, len(nodes))
        for node in notvisited.copy():
            a = random.random()
            if a < sample_p:
                samples_round[r].append(node)
                notvisited.remove(node)
        r += 1
    return samples_round

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

def labeldict(edges):
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
    return adict, ddict

def labeling(nodes, samples, r, adict, ddict):
    ancestors = {}
    descendants = {}
    for node in nodes:
        ancestors[node] = []
        descendants[node] = []
    for s in samples[r]:
        notvisit_ans = adict[s].copy()
        notvisit_des = ddict[s].copy()
        ancestors[s].append(s)
        descendants[s].append(s)
        while len(notvisit_ans) > 0:
            node = notvisit_ans.pop(0)
            ancestors[node].append(s)
            try:
                notvisit_ans.extend(adict[node])
            except:
                pass
        while len(notvisit_des) > 0:
            node = notvisit_des.pop(0)
            descendants[node].append(s)
            try:
                notvisit_des.extend(ddict[node])
            except:
                pass
    return ancestors, descendants



# A line graph
n = 100000
nodes = set(range(n))
edges = []
for i in range(n-1):
    edges.append((i, i+1)) 
# samples = set(range(100,300))
# samples_round = {}
# samples_round[1] = samples
      
adict, ddict = labeldict(edges)


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

nodes = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
samples_round = {}

s = [2, 5, 7]
samples_round[1] = s
adict, ddict = labeldict(edges)
ancestors, descendants = labeling(nodes, samples_round, 1,adict, ddict)
print("ancestors:", ancestors)
print("descendants:", descendants)

keys = ancestors.keys()
values = zip(ancestors.values(), descendants.values())
combined = dict(zip(keys, values))

        
        