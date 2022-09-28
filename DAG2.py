import math
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import itertools
import numpy as np

class Node(object):
    data = None
    aS = list()
    dS = list()
    def __init__(self, d):
	    self.data = d

# Following function from https://compucademy.net/generating-random-graphs-in-python/
# Runtime O(n^2)
def ER(n, p):
    """ER
    n: number of vertices
    p: inclusion probability
    """
    V = np.arange(n)
    
    # Create a list of E possible edges
    E = []
    for combination in numpy_combinations(V):
        a = random.random()
        if a < p:
            E.append(combination)
    
    # Create directed graph
    return V, E
    
# Helper functions
def numpy_combinations(x):
    idx = np.stack(np.triu_indices(len(x), k=1), axis=-1)
    return x[idx]


start_time = time.time()
V, E = ER(10000, 0.2)
print("--- %s seconds for generating a graph using ER ---" % (time.time() - start_time))
