from numpy import random
import numpy as np

#Здесь разместим методы стохастической оптимизации

def _generate_spot_from_simplex(dim, max_val):
    gamma = [np.random.rand() for k in range(dim)]
    spot = np.zeros(dim)

    p1 = 1
    p2 = gamma[0] ** (1 / dim)
    spot[0] = max_val * (p1 - p2)
    for i in range(1, dim):
        p1 *= gamma[i - 1] ** (1 / (dim - i + 1))
        p2 *= gamma[i] ** (1 / (dim - i))
        spot[i] = max_val * (p1 - p2)
    return spot

def optimize_by_monte_carlo():
    print('Monte Carlo Optimization')

def optimize_by_annealing():
    print('Annealing Optimisation')
