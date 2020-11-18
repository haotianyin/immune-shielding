import networkx as nx
import numpy as np
import pandas as pd
from math import floor
from SIR_network import network_model
import matplotlib.pyplot as plt

def initial_node(G, init):
    N = len(G)
    if init[1] == 0:
        Infection_number = 0
    else:
        Infection_number = floor(N*init[1]) if floor(N*init[1]) > 0 else 1

    if init[2] == 0:
        Recovered_number = 0
    else:
        Recovered_number = floor(N*init[2]) if floor(N*init[2]) > 0 else 1

    infected_node = np.random.choice(list(G.nodes), Infection_number)
    G_copy = G.copy()
    G_copy.remove_nodes_from(infected_node)
    recovered_node = np.random.choice(list(G_copy.nodes), Recovered_number)
    return [infected_node, recovered_node]


def test_budget_greedy(g, beta, gamma, init, maxt, assigned):
    # ground truth
    S, I, R = network_model(g, beta, gamma, init, maxt, assigned)
    budgets = [5, 10, 20, 30, 40, 50, None]
    R_final = []
    for budget in budgets:
        # greedy SI
        S_r, I_r, R_r = network_model(g, beta, gamma, init, maxt, assigned, budget=budget, rewire="greedy")
        R_final.append(R_r)
        print("budget : {} done".format(budget))

    df = pd.DataFrame({"Ground_Truth": R,
                       "budget=5": R_final[0],
                       "budget=10": R_final[1],
                       "budget=20": R_final[2],
                       "budget=30": R_final[3],
                       "budget=40": R_final[4],
                       "budget=50": R_final[5],
                       "budget=None": R_final[6]
                       })
    df.to_csv("Exp_budget_limit_greedy.csv", encoding='utf-8', index=False)
    return


def test_budget_greedy_eig(g, beta, gamma, init, maxt, assigned):
    budgets = [5, 10, 20, 30, 40, 50, None]
    # ground truth
    S, I, R = network_model(g, beta, gamma, init, maxt, assigned)
    R_final = []
    for budget in budgets:
        # greedy SI
        S_r, I_r, R_r = network_model(g, beta, gamma, init, maxt, assigned, budget=budget, rewire="greedy_eigen")
        R_final.append(R_r)
        print("budget : {} done".format(budget))

    df = pd.DataFrame({"Ground_Truth": R,
                       "budget=5": R_final[0],
                       "budget=10": R_final[1],
                       "budget=20": R_final[2],
                       "budget=30": R_final[3],
                       "budget=40": R_final[4],
                       "budget=50": R_final[5],
                       "budget=None": R_final[6]
                       })
    df.to_csv("Exp_budget_limit_greedyE.csv", encoding='utf-8', index=False)
    return


def test_start_time_greedy(g, beta, gamma, init, maxt, assigned):
    budgets = [5, 50]
    start_t = [10,50,100,300,500,800]
    S, I, R = network_model(g, beta, gamma, init, maxt, assigned)
    Rr = []

    for budget in budgets:
        for start in start_t:
            S_r, I_r, R_r = network_model(g, beta, gamma, init, maxt, assigned, budget=budget, rewire="greedy", start_t=start)
            Rr.append(R_r)
            print("Budget:{}, start time:{} Done".format(budget, start))
    df_d = {"Ground_Truth": R}
    for i in range(len(Rr)):
        df_d[str(i)] = Rr[i]
    df = pd.DataFrame(df_d)

    df.to_csv("Exp_start_time_greedy.csv", encoding='utf-8', index=False)

    return

def test_start_time_greedyE(g, beta, gamma, init, maxt, assigned):
    budgets = [5, 50]
    start_t = [10,50,100,300,500,800]
    S, I, R = network_model(g, beta, gamma, init, maxt, assigned)
    Rr = []

    for budget in budgets:
        for start in start_t:
            S_r, I_r, R_r = network_model(g, beta, gamma, init, maxt, assigned, budget=budget, rewire="greedy_eigen", start_t=start)
            Rr.append(R_r)
            print("Budget:{}, start time:{} Done".format(budget, start))
    df_d = {"Ground_Truth": R}
    for i in range(len(Rr)):
        df_d[str(i)] = Rr[i]
    df1 = pd.DataFrame(df_d)

    df1.to_csv("Exp_start_time_greedyE.csv", encoding='utf-8', index=False)

    return

if __name__ == "__main__":

    g = nx.read_edgelist("ia-enron-only.mtx", nodetype=int)
    init = [0.95, 0.05, 0]
    beta = 0.2
    gamma = 0.07
    maxt = 100
    assign = initial_node(g, init)

    test_budget_greedy(g, beta, gamma, init, maxt, assign)
    test_start_time_greedy(g, beta, gamma, init, maxt, assign)
    test_budget_greedy_eig(g, beta, gamma, init, maxt, assign)
    test_start_time_greedyE(g, beta, gamma, init, maxt, assign)
