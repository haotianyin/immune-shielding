import numpy as np
import copy
from collections import defaultdict
from greedySI import reduce_link
from greedySI_eigen import reduce_link_eigen
import time

def run_network(Graph, beta, gamma, node_status):
    N = Graph.number_of_nodes()
    new_status = copy.deepcopy(node_status)
    for node in Graph.nodes:
        neighbors = list(Graph.neighbors(node))
        len_neig = len(neighbors)
        p = np.random.random_sample()
        if len_neig > 0:
            if len_neig > 1:
                contact = np.random.randint(0, len_neig-1)
            else:
                contact = 0
            if node_status[node] == 0 and node_status[neighbors[contact]]:
                if p < beta:
                    new_status[node] = 1

        if node_status[node] == 1:
            if p < gamma:
                new_status[node] = 2

    S = len([i for i in Graph if new_status[i] == 0]) / N
    I = len([i for i in Graph if new_status[i] == 1]) / N
    R = len([i for i in Graph if new_status[i] == 2]) / N
    return S, I, R, new_status


def network_model(Graph, beta, gamma, init, max_time, assigned, budget=None, rewire=None, start_t=None):

    node_status = defaultdict(int)
    if rewire == "greedy":
        rewire_func = reduce_link
    elif rewire == "greedy_eigen":
        rewire_func = reduce_link_eigen

    Infection_nodes = assigned[0]
    Recovered_nodes = assigned[1]
    for n in Infection_nodes:
        node_status[n] = 1

    for n in Recovered_nodes:
        node_status[n] = 2

    S_final, I_final, R_final = [], [], []


    for sim in range(15):
        S, I, R = [init[0]], [init[1]], [init[2]]
        node_status_tmp = node_status
        if rewire is not None:
            G = Graph.copy()
        else:
            G = Graph
        for i in range(1, max_time+1):
            S_new, I_new,R_new, node_status_tmp = run_network(G, beta, gamma, node_status_tmp)
            if rewire is not None:
                if start_t is not None and i >= start_t:
                    G = rewire_func(G, node_status_tmp, budget)
                else:
                    G = rewire_func(G, node_status_tmp, budget)
            S.append(S_new)
            I.append(I_new)
            R.append(R_new)
        S_final.append(S)
        I_final.append(I)
        R_final.append(R)

    return np.mean(S_final, axis=0), np.mean(I_final, axis=0), np.mean(R_final, axis=0)
