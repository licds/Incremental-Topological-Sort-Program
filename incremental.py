from v2 import *

def modify_first_layer(label_dict, adict, ddict, edge):
    adict[edge[0]].add(edge[1])
    ddict[edge[1]].add(edge[0])
    atemp = adict[edge[0]].copy()
    atemp.add(edge[0])
    dtemp = ddict[edge[0]].copy()
    dtemp.add(edge[0])
    a_wait = []
    d_wait = []
    while len(atemp) > 0:
        node = atemp.pop()
        atemp.update(adict[node])
        a_wait.append(node)
    while len(dtemp) > 0:
        node = dtemp.pop()
        dtemp.update(ddict[node])
        d_wait.append(node)
    for node in a_wait:
        a = set(label_dict[node][0]).union(set(label_dict[edge[0]][0]))
        label_dict[node] = (tuple(a), label_dict[node][1])
    for node in d_wait:
        d = set(label_dict[node][1]).union(set(label_dict[edge[1]][1]))
        label_dict[node] = (label_dict[node][0], tuple(d))
    return label_dict

def compare_partition(origin_partition, new_partition, edge):
    refined = []
    for part in new_partition:
        if part not in origin_partition:
            refined.append(part)
        if edge[0] in part and edge[1] in part:
            refined.append(part)
    return refined

def update_label(label_dict, refined, samples, r, adict, ddict):
    for subgraph in refined:
        anc, des = labeling(subgraph, samples, r, adict, ddict)
        for node in subgraph:
            if node not in samples[r-1]:
                label_dict[r][node] = (tuple(anc[node]), tuple(des[node]))
    return label_dict

def update_all(label_dict, adict, ddict, edge, samples):
    # print("origin", label_dict)
    origin_round = label_dict.copy()
    updated = defaultdict()
    start = time.time()
    updated[1] = modify_first_layer(label_dict[1], adict, ddict, edge)
    print("modify first layer", time.time()-start)
    refined = compare_partition(partition(origin_round[1]), partition(label_dict[1]), edge)
    for r in range(2, len(samples)):
        update_label(label_dict, refined, samples, r, adict, ddict)
        refined = partition(label_dict[r])
    # print("updated", label_dict)
    return label_dict

n = 100000 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
nodes = set(range(n))
edges = []
# edges = [(0,1),(1,2),(2,7),(4,6),(5,6),(6,7)]
for i in range(n//2-1):
    edges.append((i, i+1))
for i in range(n//2, n-1):
    edges.append((i, i+1))
origin_round = {}

adict, ddict = labeldict(edges)
samples_round = newsample(nodes)
samples_round[0] = set()
# samples_round[1] = set([0,7])
# samples_round[2] = set([1,4,5,6])
# samples_round[3] = set([2,3])
# print("sample :", samples_round)
test(nodes, adict, ddict, False, samples_round, 1, origin_round)

# print("#################################################")
# labels_round = {}
# n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# nodes, edges = graph('line', n) #line, perfect
# adict, ddict = labeldict(edges)
# print("sample :", samples_round)
# test(adict, ddict, True, samples_round, 1, labels_round)

# print("#################################################")
edge = (3,4)
start = time.time()
new = update_all(origin_round, adict, ddict, edge, samples_round)
end = time.time()
print("Update time :", end-start)
# print("new :", new)
