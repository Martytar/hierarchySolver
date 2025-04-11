from numpy import random
import numpy as np

#Здесь разместим методы стохастической оптимизации


#внутренний метод для корректной работы оптимизации монте-карло на симплексе.
#Согласно размерности(dim) и максимальному значению параметров (max_val, скаляр)
#выбирает на равностороннем симлексе точку из равномерного распределения
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

def optimize_by_monte_carlo(f, specifications, spots_number):

    if spots_number <= 0:
        raise ValueError("Number of spots must be positive")

    max_spot = np.zeros(f.input_dimension)
    max_value = f.calculate(max_spot)
    for i in range(spots_number):
        spot = np.zeros(f.input_dimension)
        for spec in specifications:
            simplex_vals = _generate_spot_from_simplex(len(spec)-1, spec[-1])
            for j in range(len(spec)-1):
                spot[spec[j]] = simplex_vals[j]
        value = f.calculate(spot)
        if value > max_value:
            max_spot = spot
            max_value = value

    return max_spot


def optimize_by_annealing():
    print('Annealing Optimisation')
