# node status is a dict indicates 0: S, 1: I, 2: R
# Graph is a networkx instance
import numpy as np


def reduce_link(Graph, node_status, budget):
    SI_link = []
    R_link = []
    k_count = 0
    if budget is None:
        budget = float("inf")
    for edge in Graph.edges():
        u, v = edge
        if node_status[u] == 1 and node_status[v] == 0 or node_status[u] == 0 and node_status[v] == 1:
            SI_link.append(edge)
        elif node_status[u] == 2 and node_status[v] == 2:
            R_link.append(edge)
        elif node_status[u] == 2 and node_status[v] == 0 or node_status[u] == 0 and node_status[v] == 2:
            R_link.append(edge)

    while len(R_link) > 0 and len(SI_link) > 0 and k_count < budget:
        S_edge = SI_link.pop()
        R_edge = R_link.pop()

        if len(set(S_edge).intersection(R_edge)) == 0:
            if (S_edge[0], R_edge[0]) not in Graph.edges():
                if (S_edge[1], R_edge[1]) not in Graph.edges():
                    if (np.sum([S_edge[0], R_edge[0]]) != 1) and (
                            np.sum([S_edge[1], R_edge[1]]) != 1):  # exclude possibility to have SI after swapping
                        Graph.remove_edges_from([S_edge, R_edge])
                        Graph.add_edges_from([(S_edge[0], R_edge[0]), (S_edge[1], R_edge[1])])
                        k_count += 1
            elif (S_edge[0], R_edge[1]) not in Graph.edges():
                if (S_edge[1], R_edge[0]) not in Graph.edges():
                    Graph.remove_edges_from([S_edge, R_edge])
                    Graph.add_edges_from([(S_edge[0], R_edge[1]), (S_edge[1], R_edge[0])])
                    k_count += 1
    return Graph