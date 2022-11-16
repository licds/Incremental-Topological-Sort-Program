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
    
    for node in changed_nodes_copy:
        alist = adict[node] - sample[1]
        dlist = ddict[node] - sample[1]
        for anc in alist:
            anc_update = anc_neighbor(anc, new_adict) - samples[1]
            if label_dict[1][anc] != label_dict[1][node] and new_label_dict[1][anc] == new_label_dict[1][node]:
                for anc_node in anc_update:
                    new_label_dict[2][anc_node] = (tuple(set(new_label_dict[2][anc_node][0]).union(set(new_label_dict[2][node][0]))), new_label_dict[2][anc_node][1])
                    if new_label_dict[2][anc_node] != label_dict[2][anc_node]:
                        changed_nodes.add(anc_node)
            if label_dict[1][anc] == label_dict[1][node] and new_label_dict[1][anc] != new_label_dict[1][node]:
                for anc_node in anc_update:
                    new_label_dict[2][anc_node] = (tuple(set(new_label_dict[2][anc_node][0]).difference(set(new_label_dict[2][node][0]))), new_label_dict[2][anc_node][1])
                    if new_label_dict[2][anc_node] != label_dict[2][anc_node]:
                        changed_nodes.add(anc_node)
            if label_dict[1][anc] == label_dict[1][node] and new_label_dict[1][anc] == new_label_dict[1][node]:
                for anc_node in anc_update:
                    new_label_dict[2][anc_node] = (tuple(set(new_label_dict[2][anc_node][0]).union(set(new_label_dict[2][node][0]))), new_label_dict[2][anc_node][1])
                    if new_label_dict[2][anc_node] != label_dict[2][anc_node]:
                        changed_nodes.add(anc_node)
            
        for dec in dlist:
            dec_update = dec_neighbor(dec, new_ddict, new_label_dict, 0) - samples[1]
            if label_dict[1][dec] != label_dict[1][node] and new_label_dict[1][dec] == new_label_dict[1][node]:
                for des_node in dec_update:
                    new_label_dict[2][des_node] = (new_label_dict[2][des_node][0], tuple(set(new_label_dict[2][des_node][1]).union(set(new_label_dict[2][node][1]))))
                    if new_label_dict[2][des_node] != label_dict[2][des_node]:
                        changed_nodes.add(des_node)
            if label_dict[1][dec] == label_dict[1][node] and new_label_dict[1][dec] != new_label_dict[1][node]:
                for des_node in dec_update:
                    new_label_dict[2][des_node] = (new_label_dict[2][des_node][0], tuple(set(new_label_dict[2][des_node][1]).difference(set(new_label_dict[2][node][1]))))
                    if new_label_dict[2][des_node] != label_dict[2][des_node]:
                        changed_nodes.add(des_node)
            if label_dict[1][dec] == label_dict[1][node] and new_label_dict[1][dec] == new_label_dict[1][node]:
                for des_node in dec_update:
                    new_label_dict[2][des_node] = (new_label_dict[2][des_node][0], tuple(set(new_label_dict[2][des_node][1]).union(set(new_label_dict[2][node][1]))))
                    if new_label_dict[2][des_node] != label_dict[2][des_node]:
                        changed_nodes.add(des_node)

    changed_nodes_copy = changed_nodes.copy().union(changed_nodes_copy).difference(samples[1])
    changed_nodes = set() 
    print("changed_nodes_copy", changed_nodes_copy)
    print("###################################################")
    for node in changed_nodes_copy:
        print("Node", node, " is now being scanned")
        alist = adict[node] - samples[2] - samples[1]
        dlist = ddict[node] - samples[2] - samples[1]
        print("alist", alist)
        print("dlist", dlist)
        for anc in alist:
            print("descendant", anc, " is being evaluated")
            anc_update = anc_neighbor(anc, new_adict) - samples[2] - samples[1]
            if label_dict[2][anc] != label_dict[2][node] and new_label_dict[2][anc] == new_label_dict[2][node]:
                print("descendant is now in the same subgraph")
                for anc_node in anc_update:
                    new_label_dict[3][anc_node] = (tuple(set(new_label_dict[3][anc_node][0]).union(set(new_label_dict[3][node][0]))), new_label_dict[3][anc_node][1])
                    if new_label_dict[3][anc_node] != label_dict[3][anc_node]:
                        changed_nodes.add(anc_node)
            if label_dict[2][anc] == label_dict[2][node] and new_label_dict[2][anc] != new_label_dict[2][node]:
                print("descendant is now removed from the subgraph")
                new_label_dict[3][node] = (new_label_dict[3][node][0], tuple(set(new_label_dict[3][node][1])-anc_update))
                for anc_node in anc_update:
                    new_label_dict[3][anc_node] = (tuple(set(new_label_dict[3][anc_node][0]).difference(set(new_label_dict[3][node][0]))), new_label_dict[3][anc_node][1])
                    if new_label_dict[3][anc_node] != label_dict[3][anc_node]:
                        changed_nodes.add(anc_node)
            if label_dict[2][anc] == label_dict[2][node] and new_label_dict[2][anc] == new_label_dict[2][node]:
                print("descendant is still in the same subgraph")
                for anc_node in anc_update:
                    new_label_dict[3][anc_node] = (tuple(set(new_label_dict[3][anc_node][0]).union(set(new_label_dict[3][node][0]))), new_label_dict[3][anc_node][1])
                    if new_label_dict[3][anc_node] != label_dict[3][anc_node]:
                        changed_nodes.add(anc_node)
        for dec in dlist:
            print("ancestor", dec, " is being evaluated")
            dec_update = dec_neighbor(dec, new_ddict, new_label_dict, 1) - samples[2] - samples[1]
            print("dec_update", dec_update)
            if label_dict[2][dec] != label_dict[2][node] and new_label_dict[2][dec] == new_label_dict[2][node]:
                print("ancestor is now in the same subgraph")
                for des_node in dec_update:
                    
                    new_label_dict[3][des_node] = (new_label_dict[3][des_node][0], tuple(set(new_label_dict[3][des_node][1]).union(set(new_label_dict[3][node][1]))))
                    if new_label_dict[3][des_node] != label_dict[3][des_node]:
                        changed_nodes.add(des_node)
            if label_dict[2][dec] == label_dict[2][node] and new_label_dict[2][dec] != new_label_dict[2][node]:
                print("ancestor is now removed from the subgraph")
                new_label_dict[3][node] = (tuple(set(new_label_dict[3][node][0])-dec_update), new_label_dict[3][node][1])
                for dec_node in dec_update:
                    
                    new_label_dict[3][dec_node] = (new_label_dict[3][dec_node][0], tuple(set(new_label_dict[3][dec_node][1]).difference(set(new_label_dict[3][node][1]))))
                    if new_label_dict[3][dec_node] != label_dict[3][dec_node]:
                        changed_nodes.add(dec_node)
            print("ancestor original label", label_dict[2][dec])
            print("ancestor new label", new_label_dict[2][dec])
            print("node original label", label_dict[2][node])
            print("node new label", new_label_dict[2][node])
            if label_dict[2][dec] == label_dict[2][node] and new_label_dict[2][dec] == new_label_dict[2][node]:
                print("ancestor is now in the same subgraph")
                for des_node in dec_update:
                    print("node:", des_node, "is being updated")
                    new_label_dict[3][des_node] = (new_label_dict[3][des_node][0], tuple(set(new_label_dict[3][des_node][1]).union(set(new_label_dict[3][node][1]))))
                    if new_label_dict[3][des_node] != label_dict[3][des_node]:
                        changed_nodes.add(des_node)
                    
    for key in new_label_dict.keys():
        print(new_label_dict[key])
        
def anc_neighbor(node, adict):
    anc = set()
    anc.add(node)
    wait = set()
    wait.add(node)
    while len(wait) > 0:
        for n in adict[wait.pop()]:
            anc.add(n)
            wait.add(n)
    return anc

def dec_neighbor(node, ddict, new_label, level):
    dec = set()
    dec.add(node)
    wait = set()
    wait.add(node)
    while len(wait) > 0:
        for n in ddict[wait.pop()]:
            if level == 0:
                dec.add(n)
                wait.add(n)
            else:
                if new_label[level][node] == new_label[level][n]:
                    dec.add(n)
                    wait.add(n)
    return dec




    

n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
nodes = set(range(n))
# edges = []
edges = [(0,3),(4,5),(3,2),(6,3)]  #(1,2),(4,6),(5,6),(6,7)
# for i in range(n//2-1):
#     edges.append((i, i+1))
# for i in range(n//2, n-1):
#     edges.append((i, i+1))
origin_round = {}

adict, ddict = labeldict(edges)
samples_round = newsample(nodes)
samples_round[0] = set()
samples_round[1] = set([0,7])
samples_round[2] = set([3,1,2])
samples_round[3] = set([4,5,6])
print("sample :", samples_round)
test(nodes, adict, ddict, False, samples_round, 1, origin_round)
print(origin_round)
# print("#################################################")
# labels_round = {}
# n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# nodes, edges = graph('line', n) #line, perfect
# adict, ddict = labeldict(edges)
# print("sample :", samples_round)
# test(adict, ddict, True, samples_round, 1, labels_round)

# print("#################################################")
edge = (3,4)
# start = time.time()
# new = update_all(origin_round, adict, ddict, edge, samples_round)
# end = time.time()
# print("Update time :", end-start)
# print("#################################################")
# for i in new.keys():
#     print("Round :", i)
#     print("labels :", new[i])
#     print("")

newupdate(origin_round, adict, ddict, edge, samples_round)