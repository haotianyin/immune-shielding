#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 12:41:22 2020

@author: andreeamagalie
"""
import numpy as np
import networkx as nx
#%%
def SIR(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I  - gamma * I
    dRdt = gamma * I
    dydt = [dSdt, dIdt, dRdt]
    return dydt

#%%
'''
this function takes a degree distribution degs and returns a stack of all adj matrices 
 corresponding to that deg dist
needs to be initialized  like this because I don't know how to code:
    n = degs.size
    donts = np.zeros((n, n))
    temp_A = np.zeros((n, n))
    stack = []
'''
def degree_preserv(degs, temp_A, stack):
    #which nodes still need to be connected are the oens with positive degree
    degs_pos = np.where(degs > 0)[0] 
    #if there is nothing left to be connected, we add temp_A adj matrix to the stack
    if degs_pos.size == 0:
        temp_bs = np.copy(temp_A)
        stack.append(temp_bs)
        return stack
    
    if degs_pos.size == 1:
        return stack
    #else we look for more things to be connected
    i = degs_pos[0]
    
    y_coord = np.where(temp_A[i,:] > 0)[0]
    if y_coord.size > 0:
        y_max = np.max(y_coord)
    else:
        y_max = 0
        
    for j in degs_pos:
        if (i < j) & (temp_A[i,j] == 0) & (j >= y_max):
            #if we found two nodes to be connected
            #update the adj matrix and the donts list
            temp_A[i, j] = 1
            temp_A[j, i] = 1
            
            new_degs = np.copy(degs)
            new_degs[i] = new_degs[i] - 1
            new_degs[j] = new_degs[j] - 1
            stack = degree_preserv(new_degs, temp_A, stack)
            temp_A[i, j] = 0
            temp_A[j, i] = 0
    return stack
#%%
'''
this function takes a degree distribution degs and tells you if you can make 
a network out of it (no double edges, self loops)
Note: this is much faster if degs is in descending order
Note2: Needs to be initialized like this because I can't code:'
    n = degs.size
    donts = np.zeros((n, n))
    temp_A = np.zeros((n, n)) 
    found = False
'''
def feasible(degs, temp_A, found):
    #which nodes still need to be connected are the oens with positive degree
    degs_pos = np.where(degs > 0)[0] 
    #if there is nothing left to be connected, we add temp_A adj matrix to the stack
    if degs_pos.size == 0:
        found = True
        return found
    
    if degs_pos.size == 1:
        return False
    #else we look for more things to be connected
    i = degs_pos[0]
    
    y_coord = np.where(temp_A[i,:] > 0)[0]
    if y_coord.size > 0:
        y_max = np.max(y_coord)
    else:
        y_max = 0
        
    for j in degs_pos:
        if (i < j) & (temp_A[i,j] == 0) & (j >= y_max):
            #if we found two nodes to be connected
            #update the adj matrix and the donts list
            temp_A[i, j] = 1
            temp_A[j, i] = 1
            
            new_degs = np.copy(degs)
            new_degs[i] = new_degs[i] - 1
            new_degs[j] = new_degs[j] - 1
            found = feasible(new_degs, temp_A, found)
            if found == True:
                return found
            temp_A[i, j] = 0
            temp_A[j, i] = 0
    return False
#%%
'''
this function returns an adjacency matrix for a given degree dist
Note: Needs to be initialized like this because I can't code:'
    n = degs.size
    donts = np.zeros((n, n))
    temp_A = np.zeros((n, n)) 
    found = False
'''
def find_adj(degs, temp_A, found):
    #which nodes still need to be connected are the oens with positive degree
    degs_pos = np.where(degs > 0)[0] 
    #if there is nothing left to be connected, we add temp_A adj matrix to the stack
    if degs_pos.size == 0:
        found = True
        return temp_A
    
    if degs_pos.size == 1:
        found = False
        return 
    #else we look for more things to be connected
    i = degs_pos[0]
    
    y_coord = np.where(temp_A[i,:] > 0)[0]
    if y_coord.size > 0:
        y_max = np.max(y_coord)
    else:
        y_max = 0
        
    for j in degs_pos:
        if (i < j) & (temp_A[i,j] == 0) & (j >= y_max):
            #if we found two nodes to be connected
            #update the adj matrix and the donts list
            temp_A[i, j] = 1
            temp_A[j, i] = 1
            
            new_degs = np.copy(degs)
            new_degs[i] = new_degs[i] - 1
            new_degs[j] = new_degs[j] - 1
            found = feasible(new_degs, temp_A, found)
            if found == True:
                return temp_A
            temp_A[i, j] = 0
            temp_A[j, i] = 0
    return False
#%%
'''
Types: 0 means S, 1 means I and 2 means R
This function wants to take a degree distribution degs, node types and return 
 the adjacency matrix that minimizes the number of SI edges
HOWEVER it does not do that. It just attaches I to R preferentially so it gives back
an okay (?) matrix not an optimal one

example initialized:
    degs = np.ones(4)
    types = np.array([0,0,1,2])
    A = np.zeros((4,4))
'''
def find_min_adj(degs, types, A):
    n = degs.size
    
    I_nodes = np.where(types == 1)[0]
    R_nodes = np.where(types == 2)[0]
    #if I can make a connection between I and R 
    if (np.sum(degs[I_nodes]) > 0) and (np.sum(degs[R_nodes]) > 0):
        I0 = I_nodes[0]
        R0 = R_nodes[0]
        new_degs = np.copy(degs)
        #connect I_nodes[0] with R_nodes[0]
        new_degs[I0] = new_degs[I0] - 1
        new_degs[R0] = new_degs[R0] - 1
        if feasible(new_degs, np.zeros((n, n)), False):
            A = find_min_adj(new_degs, types, A)
            A[I0, R0] = 1
            A[R0, I0] = 1
    #otherwise not else we can do so we return anything that works 
    else:
        return find_adj(degs, np.zeros((n,n)), False)
    return A
#%%
# This function takes a regular network of size n where every degree is k,
# and node types and gives back an adj matrix with minimimun number
#of SI edges
def find_min_adj_reg(G, types):
    n = G.number_of_nodes()
    k = [val for (node, val) in G.degree([0])][0]
    degs = k * np.ones(n)
    S_nodes = np.where(types == 0)[0]
    I_nodes = np.where(types == 1)[0]
    not_I = np.where(types != 1)[0]
    n_I = I_nodes.size # number of infected individuals
    R_nodes = np.where(types == 2)[0]
    n_R = R_nodes.size #number of recovered individuals
    A = np.zeros((n ,n))
    if n_I == 0:
        A = find_adj(degs, A, False)
        return nx.from_numpy_matrix(A)
    if n_I > k:
        # we can connect all I edges with other I nodes
        temp_degs = np.copy(degs)
        for val in not_I:
            temp_degs[val] = 0
        temp_A = find_adj(temp_degs, np.zeros((n, n)), False)
        A = A + temp_A
        
        #connect the rest
        temp_degs = np.copy(degs)
        for val in I_nodes:
            temp_degs[val] = 0
        
        temp_A = find_adj(temp_degs, np.zeros((n, n)), False)
        A = A + temp_A
    else:
        diff = k - n_I + 1 # left to connect
        if n_R >= diff:
            # we connect all I nodes with the other I nodes but there are still
            # diff (k - n_I + 1) to connect and we will connect these with R nodes
            temp_degs = np.copy(degs)
            for val in S_nodes:
                temp_degs[val] = 0
            for val in I_nodes:
                temp_degs[val] = k
            for val in range(diff):
                temp_degs[R_nodes[val]] = n_I
            
            temp_A = find_adj(temp_degs, np.zeros((n, n)), False)
            A = A + temp_A
            
            # connect the rest
            temp_degs = np.copy(degs)
            for val in I_nodes:
                temp_degs[val] = 0
            for val in range(diff):
                temp_degs[R_nodes[val]] = k - n_I
            for val in range(diff, n_R):
                temp_degs[val] = k
            #print(temp_degs)
            temp_A = find_adj(temp_degs, np.zeros((n, n)), False)
            #print('reached')
            A = A + temp_A
        
        #we must have some SI connections in this case 
        #we connect I nodes with all other I and R nodes and then connect 
        #the rest with S nodes 
        else:
            temp_degs = np.copy(degs)
            for val in S_nodes:
                temp_degs[val] = 0
            for val in I_nodes:
                temp_degs[val] = n_I + n_R - 1
            for val in R_nodes:
                temp_degs[val] = n_I
                       
            temp_A = find_adj(temp_degs, np.zeros((n, n)), False)

            #connect the rest
            #n_R < k - n_I + 1
            #n_I <= k
            temp_degs = np.copy(degs)
            for val in S_nodes:
                temp_degs[val] = k
            for val in I_nodes:
                temp_degs[val] = k - (n_I + n_R - 1)
            for val in R_nodes:
                temp_degs[val] = k - n_I

            temp_A = find_adj(temp_degs, temp_A, False)

            A = A + temp_A
    return nx.from_numpy_matrix(A)