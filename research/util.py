# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import numpy.random as rand

def rchoice(weights):
    """Makes a (weighted) random choice.
    
    Given a vector of probabilities with a total sum of 1, this function 
    returns the index of one element of the list with probability equal to 
    this element's value. For example, given the vector [0.2, 0.5, 0.3], the 
    probability that the function returns 0 is 20%, the probability that 
    the functions returns 1 is 50% and the probability that it returns 2 
    is 30%.
    
    Args:
        weights (1xN array): The vector with the probability of each index
    
    Returns:
        The randomly chosen index
    """
    
    positive_probs = np.nonzero(weights)[0]
    s = 0.0
    r = rand.random()
    
    for i in positive_probs:
        s += weights[i]
        if r <= s:
            return i
    
    raise RuntimeError('Failed to make a random choice. Check input vector.')

def rowStochastic(A):
    """Makes a matrix row (right) stochastic.
    
    Given a real square matrix, returns a new matrix which is right 
    stochastic, meaning that each of its rows sums to 1.
    
    Args: 
        A (NxN numpy array): The matrix to be converted
    
    Returns:
        A NxN numpy array which is row stochastic.
    """
    
    return A/A.sum(axis=1, keepdims = True)
    
    
def randomSpanningTree(N, rand_weights = False):
    """Creats a graph of N nodes connected by a random spanning tree.
    
    Args:
        N (int): Number of nodes
    
    Returns:
        A NxN numpy array representing the adjacency matrix of the graph.
    """

    nodes = rand.permutation(N)
    A = np.zeros((N, N))
    
    for i in range(1, N):
        w = rand.random() if rand_weights else 1
        A[nodes[i-1],nodes[i]] = w
        A[nodes[i],nodes[i-1]] = w

    return A
    
def meanDegree(A):
    """Calculates the mean degree of a graph.
    
    Args:
        A (NxN numpy array): The adjacency matrix of the graph
    
    Returns:
        The mean degree of the graph.
    """
    B = np.empty_like(A)
    np.copyto(B,A)
    B[B > 0] = 1
    degrees = B.sum(axis=1)
    return np.mean(degrees)
    
def gnp(N, p, rand_weights = False, verbose = False):
    """Constructs an undirected connected G(N, p) network with random weights.
    
    Args:
        N (int): Number of nodes
        p (double): The probability that each vertice is created
        verbose (bool): Choose whether to print the size and the mean 
            degree of the network
    Returns:
        A NxN numpy array representing the adjacency matrix of the graph.
    """
    
    A = randomSpanningTree(N)
    for i in range(N):
        for j in range(N):
            r = rand.random()
            if r < p:
                w = rand.random() if rand_weights else 1
                A[i, j] = w
                A[j, i] = w
                
    if verbose:
        print('G(N,p) Network Created: N = {N}, Mean Degree = {deg}'.format(N = N, deg = meanDegree(A)))
        
    return A
    

def plotOpinions(opinions, title='', dcolor = False):
    """Creates a plot of the opinions over time
    
    Args:
        opinions (txN vector): Vector of the opinions over time
        title (string): Optional title of the plot (default: '')
        dcolor (bool): Color the plot lines depending on the value of 
        each opinion (default: False)
    
    """
    max_rounds = np.shape(opinions)[0]
    opinion_number = np.shape(opinions)[1]
    for t in range(0, opinion_number):
        x = range(0, max_rounds)
        y = opinions[:,t]
        if dcolor:
            plt.scatter(x, y, c = cm.winter(y), edgecolor='none')
        else:
            plt.plot(range(0, max_rounds), opinions[:,t])
    plt.ylabel('Opinion')
    plt.xlabel('t')
    plt.title(title)
    plt.axis((0, max_rounds, opinions.min() - 0.1, opinions.max() + 0.1))
    plt.show()