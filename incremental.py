from v2 import *
import copy

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

def layer(changed_nodes_copy, allneighbors, completed_samples, r, new_adict, new_ddict, label_dict, new_label_dict, changed_nodes):
    for node in changed_nodes_copy:
        alist = adict[node] - completed_samples
        dlist = ddict[node] - completed_samples
        for anc in alist:
            # Getting all the descendants of the node excluding sampled nodes
            anc_update = anc_neighbor(anc, new_adict, new_label_dict, r-2) - completed_samples
            if label_dict[r-1][anc] != label_dict[r-1][node]:
                if new_label_dict[r-1][anc] == new_label_dict[r-1][node]:
                    # In this case, the node is now added into the subgraph
                    for anc_node in anc_update:
                        # We will need to add the node's ancestor label to all its descendants
                        new_label_dict[r][anc_node] = (tuple(set(new_label_dict[r][anc_node][0]).union(set(new_label_dict[r][node][0]))), new_label_dict[r][anc_node][1])
                        if new_label_dict[r][anc_node] != label_dict[r][anc_node]:
                            # Add changed nodes for next round's evaluation
                            changed_nodes.add(anc_node)
            else:
                if new_label_dict[r-1][anc] != new_label_dict[r-1][node]:
                    # In this case, an existing element is now removed from the subgraph
                    for anc_node in anc_update:
                        # We will need to remove the node's ancestor label from all its descendants
                        new_label_dict[r][anc_node] = (tuple(set(new_label_dict[r][anc_node][0]).difference(set(new_label_dict[r][node][0]))), new_label_dict[r][anc_node][1])
                        if new_label_dict[r][anc_node] != label_dict[r][anc_node]:
                            changed_nodes.add(anc_node)
                else:
                    # In this case, the subgraph remains unchanged but the incremental edge is not affecting the labels yet
                    for anc_node in anc_update:
                        # We will need to add the node's ancestor label to all its descendants in case the node has a different label
                        new_label_dict[r][anc_node] = (tuple(set(new_label_dict[r][anc_node][0]).union(set(new_label_dict[r][node][0]))), new_label_dict[r][anc_node][1])
                        if new_label_dict[r][anc_node] != label_dict[r][anc_node]:
                            changed_nodes.add(anc_node)
        for dec in dlist:
            dec_update = dec_neighbor(dec, new_ddict, new_label_dict, r-2) - completed_samples
            if label_dict[r-1][dec] != label_dict[r-1][node]:
                if new_label_dict[r-1][dec] == new_label_dict[r-1][node]:
                    # In this case, the node is now added into the subgraph
                    for des_node in dec_update:
                        # We will need to add the node's descendant label to all its ancestors
                        new_label_dict[r][des_node] = (new_label_dict[r][des_node][0], tuple(set(new_label_dict[r][des_node][1]).union(set(new_label_dict[r][node][1]))))
                        if new_label_dict[r][des_node] != label_dict[r][des_node]:
                            changed_nodes.add(des_node)
            else:
                if new_label_dict[r-1][dec] != new_label_dict[r-1][node]:
                    # In this case, an existing element is now removed from the subgraph
                    for des_node in dec_update:
                        # We will need to remove the node's descendant label from all its ancestors
                        new_label_dict[r][des_node] = (new_label_dict[r][des_node][0], tuple(set(new_label_dict[r][des_node][1]).difference(set(new_label_dict[r][node][1]))))
                        if new_label_dict[r][des_node] != label_dict[r][des_node]:
                            changed_nodes.add(des_node)
                else:
                    # In this case, the subgraph remains unchanged but the incremental edge is not affecting the labels yet
                    for des_node in dec_update:
                        # We will need to add the node's descendant label to all its ancestors in case the node has a different label
                        new_label_dict[r][des_node] = (new_label_dict[r][des_node][0], tuple(set(new_label_dict[r][des_node][1]).union(set(new_label_dict[r][node][1]))))
                        if new_label_dict[r][des_node] != label_dict[r][des_node]:
                            changed_nodes.add(des_node)

def newupdate(label_dict, adict, ddict, edge, samples):
    new_adict = adict.copy()
    new_ddict = ddict.copy()
    new_adict[edge[0]].add(edge[1])
    new_ddict[edge[1]].add(edge[0])
    new_label_dict = copy.deepcopy(label_dict)
    
    anc_update = set()
    dec_update = set()
    changed_nodes = set()
    edge_nodes = set()
    edge_nodes.add(edge[0])
    edge_nodes.add(edge[1])

    # First layer
    if new_label_dict[1][edge[0]][0] != tuple():
        anc_update = set(new_adict[edge[0]])
        wait = set(new_adict[edge[0]])
        while len(wait) > 0:
            for node in new_adict[wait.pop()]:
                anc_update.add(node)
                wait.add(node)
    if new_label_dict[1][edge[1]][1] != tuple():
        dec_update = set(new_ddict[edge[1]])
        wait = set(new_ddict[edge[1]])
        while len(wait) > 0:
            for node in new_ddict[wait.pop()]:
                dec_update.add(node)
                wait.add(node)

    if anc_update != set():
        for node in anc_update:
            new_label_dict[1][node] = (tuple(set(new_label_dict[1][node][0]).union(set(new_label_dict[1][edge[0]][0]))), new_label_dict[1][node][1])
            if new_label_dict[1][node] != label_dict[1][node]:
                changed_nodes.add(node)
    if dec_update != set():
        for node in dec_update:
            new_label_dict[1][node] = (new_label_dict[1][node][0], tuple(set(new_label_dict[1][node][1]).union(set(new_label_dict[1][edge[1]][1]))))
            if new_label_dict[1][node] != label_dict[1][node]:
                changed_nodes.add(node)
    
    changed_nodes.update(edge_nodes)
    changed_nodes_copy = changed_nodes.copy()
    changed_nodes = set() 
    completed_samples = samples[1]

    # Remaining layers
    start = time.time()
    for i in range(2, len(samples)):
        layer(changed_nodes_copy, completed_samples, i, new_adict, new_ddict, label_dict, new_label_dict, changed_nodes)
        changed_nodes_copy = changed_nodes.copy().union(changed_nodes_copy).difference(completed_samples)
        changed_nodes = set() 
        completed_samples = completed_samples.union(samples[i])
    print(time.time() - start)
                    
    # for key in new_label_dict.keys():
    #     print(new_label_dict[key])
        
def allneighbors(nodes,adict,ddict):
    neighbors = defaultdict(list)
    for node in nodes:
        anc = []
        dec = []
        anc.append(node)
        dec.append(node)
        wait = []
        wait.append(node)
        while len(wait) > 0:
            for n in adict[wait.pop()]:
                anc.append(n)
                wait.append(n)
        wait.append(node)
        while len(wait) > 0:
            for n in ddict[wait.pop()]:
                dec.append(n)
                wait.append(n)
        neighbors[node] = [anc,dec]
    return neighbors

def anc_neighbor(node, adict, new_label, r):
    anc = set()
    anc.add(node)
    wait = set()
    wait.add(node)
    while len(wait) > 0:
        for n in adict[wait.pop()]:
            if r == 0:
                anc.add(n)
                wait.add(n)
            else:
                try:
                    if new_label[r][node] == new_label[r][n]:
                        anc.add(n)
                        wait.add(n)
                except:
                    break
    return anc

def dec_neighbor(node, ddict, new_label, r):
    dec = set()
    dec.add(node)
    wait = set()
    wait.add(node)
    while len(wait) > 0:
        for n in ddict[wait.pop()]:
            if r == 0:
                dec.add(n)
                wait.add(n)
            else:
                try:
                    if new_label[r][node] == new_label[r][n]:
                        dec.add(n)
                        wait.add(n)
                except:
                    break
    return dec




    
### DEBUGGING/CORRECTNESS BLOCK ###
n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
nodes = set(range(n))
edges = [(0,3),(4,5),(3,2),(6,3)]  #(1,2),(4,6),(5,6),(6,7)
origin_round = {}

adict, ddict = labeldict(edges)
samples_round = defaultdict(set)
samples_round[0] = set()
samples_round[1] = set([0,7])
samples_round[2] = set([3,1,2])
samples_round[3] = set([4,5,6])
print("sample :", samples_round)
test(nodes, adict, ddict, False, samples_round, 1, origin_round)

allneighbors = allneighbors(nodes,adict,ddict)
edge = (3,4)
newupdate(origin_round, adict, ddict, edge, samples_round)

### TESTING BLOCK
# n = 1000 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# nodes = set(range(n))
# edges = []
# for i in range(n//2-1):
#     edges.append((i, i+1))
# for i in range(n//2, n-1):
#     edges.append((i, i+1))
# origin_round = {}

# adict, ddict = labeldict(edges)
# samples_round = newsample(nodes)
# samples_round[0] = set()
# test(nodes, adict, ddict, False, samples_round, 1, origin_round)

# edge = (n//2-1, n//2)
# start = time.time()
# newupdate(origin_round, adict, ddict, edge, samples_round)
# end = time.time()
# print("Update time :", end-start)