import math
import random
import time
import pickle
from collections import defaultdict


### 生成每轮的sample, sample_rate --> sample --> newsample ###
# 设置sample rate
def sample_rate(power, n):
    sample_p = (math.log(n))**power/n
    return sample_p

# 从nodes中随机抽取sample的节点
def sample(nodes, sample_p):
    S = set()
    for node in nodes:
        a = random.random()
        if a < sample_p:
            S.add(node)
    return S

# 生成每一轮的sample
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

### 生成每轮的label, label_rate --> label --> newlabel ###
# 通过edge为每个node找到直接连接的ancestor和descendant
def labeldict(edges):
    adict = defaultdict(set)
    ddict = defaultdict(set)
    for edge in edges:
        adict[edge[0]].add(edge[1])
        ddict[edge[1]].add(edge[0])
    return adict, ddict

# 生成每个node的ancestor和descendant label
def labeling(nodes, samples, r, adict, ddict):
    ancestors = {}
    descendants = {}
    tempdict = {}
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

# 合并label： 取ancestor dictionary和descendant dictionary的交集作为combined dictionary
def label(ancestors, descendants, samples):
    keys = set(ancestors.keys()) - samples
    combined = {}
    for key in keys:
        combined[key] = [set(ancestors[key]), set(descendants[key])] #combined dictionary 的格式
    return combined

# 根据label做partition
def partition(combined):
    part_dict = defaultdict(set)
    parts = list(combined.items())
    for part in parts:
        a = (tuple(part[1][0]),tuple(part[1][1]))
        part_dict[a].add(part[0])
    subgraphs = [set(part) for part in part_dict.values()]
    return subgraphs

# 生成图，目前仅包含line和perfect binary tree
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
    # trials 仅为测试平均速度用
    for i in range(trials):
        begin = time.time()
        i = 1
        subgraphs = [nodes] #初始化subgraphs，所有node为一个subgraph
        while len(subgraphs) > 0:
            if out == True:
                print("Round", i, ":", subgraphs)
            ancestors = {}
            descendants = {}
            graphs = []
            for subgraph in subgraphs:
                start = time.time()
                anc, des = labeling(subgraph, samples_round, i, adict, ddict) #创建 subgraph的 ancestor和descendant dictionary
                label_time += time.time()-start
                start = time.time()
                combined = label(anc, des, samples_round[i]) #合并 subgraph 的ancestor和descendant dictionary
                label_time += time.time()-start
                start = time.time()
                graph = partition(combined) #根据label做partition
                graphs.extend(graph) #将partition后的subgraph加入subgraphs
                partition_time += time.time()-start 
                start = time.time()
                ancestors.update(anc) #更新 subgraphs 的ancestor dictionary
                descendants.update(des) #更新 subgraphs 的descendant dictionary
                label_time += time.time()-start
            start = time.time()
            combined = label(ancestors, descendants, samples_round[i-1]) #合并 subgraphs 的ancestor和descendant dictionary
            label_time += time.time()-start
            if out == True:
                print("labels :", combined)
            labels_round.append(combined) #将labels加入输出的labels_round
            start = time.time()
            subgraphs = graphs #更新subgraphs
            partition_time += time.time()-start
            i += 1
        total_time += time.time()-begin
    print("label_time:", label_time/trials)
    print("partition_time:", partition_time/trials)
    print("total_time:", total_time/trials)

<<<<<<< Updated upstream:v2.py
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
=======
#### 测试 ####

################################################################################################
### 测试8个节点的正确性 ###
# # n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071 设置节点数
# # # nodes, edges = graph('line', n) #line, perfect 设置图类型
# # nodes = set(range(n)) #设置节点
# # edges = [(0,1),(1,2),(2,3),(4,5),(5,6),(6,7)] #设置边 仅用于8个节点line graph
# # labels_round = {}

# # #载入存储的图
# # # with open('perfect_graph.txt', 'w') as f:
# # #     f.write(str(nodes))
# # #     f.write('\n')
# # #     f.write(str(edges))
# # # with open('line_graph100000.txt') as f:
# # #     nodes_line = f.readline()
# # #     nodes = eval(nodes_line)
# # #     edges_line = f.readline()
# # #     edges = eval(edges_line)

# # adict, ddict = labeldict(edges)
# # samples_round = newsample(nodes)
# # samples_round[0] = set()
# # samples_round[1] = set([0, 7])
# # samples_round[2] = set([1,4,5,6])
# # samples_round[3] = set([2,3])
# # print("sample :", samples_round)
# # test(adict, ddict, True, samples_round, 1, labels_round)
# # # print("labels_round :", labels_round)
# # print("#################################################")
################################################################################################

################################################################################################
# ### 测试若干节点的速度 ###
# n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
# nodes, edges = graph('line', n) #line, perfect
# adict, ddict = labeldict(edges)
# samples_round = newsample(nodes)
# labels_round = []
# labels_round.append([])
>>>>>>> Stashed changes:preincremental.py
# samples_round[0] = set()
# samples_round[1] = set([0, 7])
# samples_round[2] = set([1,4,5,6])
# samples_round[3] = set([2,3])
<<<<<<< Updated upstream:v2.py
# print("sample :", samples_round)
# test(adict, ddict, True, samples_round, 1, labels_round)
# # print("labels_round :", labels_round)
# print("#################################################")

n = 8 #1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535,131071
nodes, edges = graph('line', n) #line, perfect
adict, ddict = labeldict(edges)
samples_round = newsample(nodes)
labels_round = []
labels_round.append([])
samples_round[0] = set()
samples_round[1] = set([0, 7])
samples_round[2] = set([1,4,5,6])
samples_round[3] = set([2,3])

print("sample :", samples_round)
test(nodes, adict, ddict, True, samples_round, 1, labels_round)
print("labels_round :", labels_round)

=======

# print("sample :", samples_round)
# test(nodes, adict, ddict, True, samples_round, 1, labels_round)
# print("labels_round :", labels_round)
################################################################################################
>>>>>>> Stashed changes:preincremental.py






