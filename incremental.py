from v2 import *
import copy

def layer(changed_nodes_copy,  completed_samples, r, new_adict, new_ddict, label_dict, new_label_dict, changed_nodes):
    neighbor_time = 0
    dec_neighbors = defaultdict(list)
    anc_neighbors = defaultdict(list)
    for node in changed_nodes_copy:
        decendant_list = new_adict[node] - completed_samples
        ancestor_list = new_ddict[node] - completed_samples
        for dec in decendant_list:
            # Getting all the descendants of the node excluding sampled nodes
            start = time.time()
            # Find all the neighbors of the decendant
            if dec not in dec_neighbors:
                dec_neighbors[dec] = neighbor(dec, new_adict, new_label_dict, r-2, completed_samples) - completed_samples
            dec_update = dec_neighbors[dec]
            neighbor_time += time.time() - start
            
            # Check if the decendant is in the same subgraph with the node in the previous round before we add the edge
            if label_dict[r-1][dec] != label_dict[r-1][node]:

                # Check if the descendant is in the same subgraph with the node in the previous round after we add the edge
                if new_label_dict[r-1][dec] == new_label_dict[r-1][node]:

                    # In this case, the node is now added into the subgraph; we need to loop through the neighbors of the decendant and add the node's ancestors to them
                    for dec_neighbor in dec_update:
                        # For each neighbor, we use original ancestors and the node's ancestors to update its ancestors, its decendants remain unchanged
                        new_label_dict[r][dec_neighbor][0] = new_label_dict[r][dec_neighbor][0].union(new_label_dict[r][node][0])

                        # For each neighbor, we will need to take its decendants and add them to the node's decendants
                        new_label_dict[r][node][1] = new_label_dict[r][node][1].union(new_label_dict[r][dec_neighbor][1])

                        find_changed_node(node, new_label_dict, label_dict, r, changed_nodes)
                        find_changed_node(dec_neighbor, new_label_dict, label_dict, r, changed_nodes)

            # If the decendant is in the same subgraph with the node in the previous round before we add the edge
            else:

                # Check if the descendant departs from the subgraph after we add the edge
                if new_label_dict[r-1][dec] != new_label_dict[r-1][node]:

                    # In this case, the node is removed from the subgraph; we need to loop through the neighbors of the decendant and remove the node's ancestors from them
                    for dec_neighbor in dec_update:

                        # We will need to remove the node's ancestor label from all its descendants
                        new_label_dict[r][dec_neighbor][0] = new_label_dict[r][dec_neighbor][0].difference(new_label_dict[r][node][0])

                        # For each neighbor, we will need to take its decendants and remove them from the node's decendants
                        new_label_dict[r][node][1] = new_label_dict[r][node][1].difference(new_label_dict[r][dec_neighbor][1])

                        find_changed_node(node, new_label_dict, label_dict, r, changed_nodes)
                        find_changed_node(dec_neighbor, new_label_dict, label_dict, r, changed_nodes)
                        
        for anc in ancestor_list:
            # Getting all the ancestors of the node excluding sampled nodes
            start = time.time()
            if anc not in anc_neighbors:
                anc_neighbors[anc] = neighbor(anc, new_ddict, new_label_dict, r-2, completed_samples) - completed_samples
            anc_update = anc_neighbors[anc]
            neighbor_time += time.time() - start

            # Check if the ancestor is in the same subgraph with the node in the previous round before we add the edge
            if label_dict[r-1][anc] != label_dict[r-1][node]:

                # Check if the ancestor is in the same subgraph with the node in the previous round after we add the edge
                if new_label_dict[r-1][anc] == new_label_dict[r-1][node]:

                    # In this case, the node is now added into the subgraph; we need to loop through the neighbors of the ancestor and add the node's descendants to them
                    for anc_neighbor in anc_update:

                        # For each neighbor, we use original descendants and the node's descendants to update its descendants, its ancestors remain unchanged
                        new_label_dict[r][anc_neighbor][1] = new_label_dict[r][anc_neighbor][1].union(new_label_dict[r][node][1])

                        # For each neighbor, we will need to take its ancestors and add them to the node's ancestors
                        new_label_dict[r][node][0] = new_label_dict[r][node][0].union(new_label_dict[r][anc_neighbor][0])

                        find_changed_node(node, new_label_dict, label_dict, r, changed_nodes)
                        find_changed_node(anc_neighbor, new_label_dict, label_dict, r, changed_nodes)
            
            # If the ancestor is in the same subgraph with the node in the previous round before we add the edge
            else:

                # Check if the ancestor departs from the subgraph after we add the edge
                if new_label_dict[r-1][anc] != new_label_dict[r-1][node]:

                    # In this case, the node is removed from the subgraph; we need to loop through the neighbors of the ancestor and remove the node's descendants from them
                    for anc_neighbor in anc_update:

                        # We will need to remove the node's descendant label from all its ancestors
                        new_label_dict[r][anc_neighbor][1] = new_label_dict[r][anc_neighbor][1].difference(new_label_dict[r][node][1])

                        # For each neighbor, we will need to take its ancestors and remove them from the node's ancestors
                        new_label_dict[r][node][0] = new_label_dict[r][node][0].difference(new_label_dict[r][anc_neighbor][0])

                        find_changed_node(node, new_label_dict, label_dict, r, changed_nodes)
                        find_changed_node(anc_neighbor, new_label_dict, label_dict, r, changed_nodes)
    return neighbor_time

def find_changed_node(node, new_label_dict, label_dict, r, changed_nodes):
    if new_label_dict[r][node] != label_dict[r][node]:
        changed_nodes.add(node)

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
    if new_label_dict[1][edge[0]][0] != set():
        anc_update = set(new_adict[edge[0]])
        wait = set(new_adict[edge[0]])
        while len(wait) > 0:
            for node in new_adict[wait.pop()]:
                anc_update.add(node)
                wait.add(node)
    if new_label_dict[1][edge[1]][1] != set():
        dec_update = set(new_ddict[edge[1]])
        wait = set(new_ddict[edge[1]])
        while len(wait) > 0:
            for node in new_ddict[wait.pop()]:
                dec_update.add(node)
                wait.add(node)

    if anc_update != set():
        for node in anc_update:
            new_label_dict[1][node][0] = new_label_dict[1][node][0].union(new_label_dict[1][edge[0]][0])
            if new_label_dict[1][node] != label_dict[1][node]:
                changed_nodes.add(node)
    if dec_update != set():
        for node in dec_update:
            new_label_dict[1][node][1] = new_label_dict[1][node][1].union(new_label_dict[1][edge[1]][1])
            if new_label_dict[1][node] != label_dict[1][node]:
                changed_nodes.add(node)

    num_labelchanged = 0
    changed_nodes_copy = changed_nodes.copy()
    num_labelchanged += len(changed_nodes_copy)
    total_changed = set()
    total_changed.update(changed_nodes_copy)
    changed_nodes_copy = edge_nodes
    total_changed.update(changed_nodes_copy)

    changed_nodes = set() 
    completed_samples = samples[1]

    # Remaining layers
    neighbor_time = 0
    for i in range(2, len(samples)):
        neighbor_time += layer(changed_nodes_copy, completed_samples, i, new_adict, new_ddict, label_dict, new_label_dict, changed_nodes)
        changed_nodes_copy = changed_nodes.copy().union(changed_nodes_copy).difference(completed_samples)
        total_changed.update(changed_nodes_copy)
        changed_nodes = set() 
        completed_samples = completed_samples.union(samples[i])
    print("Neighbor time: ", neighbor_time)

    print("Number of node changes: ", len(total_changed))
                    
    # for key in new_label_dict.keys():
    #     print(new_label_dict[key])
    return new_label_dict
        
def neighbor(node, dict, new_label, r, samples):
    neigh = set()
    neigh.add(node)
    wait = set()
    wait.add(node)
    if r == 0:
        while len(wait) > 0:
            for n in dict[wait.pop()]:
                neigh.add(n)
                wait.add(n)
        return neigh
    while len(wait) > 0:
        for n in dict[wait.pop()]:
            if n not in samples:
                if new_label[r][node] == new_label[r][n]:
                    neigh.add(n)
                    wait.add(n)
    return neigh

    
### DEBUGGING/CORRECTNESS BLOCK ###
# n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# nodes = set(range(n))
# edges = [(0,3),(1,2),(2,3),(4,6),(5,6),(6,7)]  #(1,2),(4,6),(5,6),(6,7)
# # edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15)]
# origin_round = {}

# adict, ddict = labeldict(edges)
# samples_round = defaultdict(set)
# samples_round[0] = set()
# samples_round[1] = set([0,7])
# samples_round[2] = set([1,2,3])
# samples_round[3] = set([4,5,6])
# # samples_round[4] = set([8,7,10,11,12,13,14,15])
# test(nodes, adict, ddict, False, samples_round, 1, origin_round)

# edge = (3,4)
# new_label = newupdate(origin_round, adict, ddict, edge, samples_round)

# for i in range(1, len(origin_round)+1):
#     print("Sample", i, ":", samples_round[i])
#     print("Origin Round", i, ":", origin_round[i])
#     print("New round", i, ":", new_label[i])

### TESTING BLOCK
n = 10000 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
nodes = set(range(n))
edges = []
for i in range(n//2-1):
    edges.append((i, i+1))
for i in range(n//2, n-1):
    edges.append((i, i+1))
origin_round = []
origin_round.append([])

adict, ddict = labeldict(edges)
samples_round = newsample(nodes)
samples_round[0] = set()
for round in range(1, len(samples_round)):
    print("Round", round, ":", len(samples_round[round]))
test(nodes, adict, ddict, False, samples_round, 1, origin_round)


edge = (n//2-1, n//2)

start = time.time()
new_label = newupdate(origin_round, adict, ddict, edge, samples_round)
end = time.time()
print("Update time :", end-start)

# for z in range(1, len(origin_round)+1):
#     print("Round:",z)
#     print(samples_round[z])
#     for i in range(498,502):
#         print("node is",i)
#         print(origin_round[z][i])
#         print(new_label[z][i])
#         print()
# for i in range(1, len(origin_round)+1):
#     print("Sample", i, ":", samples_round[i])
#     print("Origin Round", i, ":", origin_round[i])
#     print("New round", i, ":", new_label[i])
