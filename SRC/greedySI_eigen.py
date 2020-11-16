import numpy as np
from networkx import adjacency_matrix
import scipy


def get_W(G):

    A = adjacency_matrix(G).todense().astype(np.float32) #adjacency matrix of colocation networks
    n = A.shape[0]
    w, V,_ = scipy.linalg.eig(A, left=True)  #left leading eigenvector

    p = V[:,np.argmax(w)]

    _, q = scipy.linalg.eigh(A, eigvals=(n-1,n-1))  # right leading eigenvector

    return np.outer(p,q)


def reduce_link_eigen(Graph, node_status, budget):
    # Get W

    W = get_W(Graph)

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

    # sort SI_link based on W
    SI_link = sorted(SI_link, key=lambda x: W[x[0] - 1, x[1] - 1])  # ascending order
    R_link = sorted(R_link, key=lambda x: W[x[0] - 1, x[1] - 1])  # descending order

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
