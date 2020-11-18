the main function is used to test 2 experiments on Greedy SI and Greedy SI+(greedySI_eigen)

if directly run main it will run 4 experiment in order of budget control for greedySI, start time control for greedy SI, budget control for greedySI+, and finally start time control for greedy SI+. 

Each experiment will produce a csv file. Exp_budget_limit_greedy.csv and Exp_budget_limit_greedyE.csv contains 8 columns. column 1 is the ground truth.

Exp_start_time_greedy and Exp_start_time_greedyE will have 13 columns. Colum 1 is the ground truth Column 2-7 are time variant with budget 5. And Column s 8-13 are result of time variant with budget 50

To test the rewire:
    please have the parameters well defined

    g = nx.read_edgelist("ia-enron-only.mtx", nodetype=int) # 1 indexed network
    init = [0.99, 0.1, 0] // initial fraction
    beta = 0.2/24 //infection rate
    gamma = 0.07/24 // recover rate
    maxt = 50*24 //time step in h
    assign = initial_node(g, init) //initial node

    to test single instance without any rewiring:
    call: network_model(g, beta, gamma, init, max_time, assigned) in main

    to test single instance of greedy SI:
     network_model(g, beta, gamma, init, max_time, assigned, rewire="greedy")

   to test single instance of greedy SI+:
     network_model(g, beta, gamma, init, max_time, assigned, rewire="greedy_eigen")

   to try out different budget:
     network_model(g, beta, gamma, init, max_time, assigned, rewire=rewire, budget=budget)

   to set start time of rewire :
     network_model(g, beta, gamma, init, max_time, assigned, rewire=rewire, budget=budget, start_t=t)

network_model will return averaged S,I, R value for 15 simulations. The Relation could be viewed using matplotlib.pyplot
by calling plt.plot([i for i in range(maxt+1)], R)
plt.show()

greedySI_eigen contains code for greedySI+
greedySI contains code for greedySI
SIR_network contains simple SIR network

my_functions contains a series of functions that manipulates the adj matrix. 