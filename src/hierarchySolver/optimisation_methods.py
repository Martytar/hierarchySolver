import copy
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

def _generate_spot_fast_annealing(spot, T, b):
    dim = len(spot)
    new_spot = copy.deepcopy(spot)

    l = 2*b
    c = 0
    new_spot_sum = 0

    for i in range(dim):
        a = np.random.rand()
        z = np.sign(a - 0.5) * T * ((1 + 1.0 / T) ** (np.abs(2 * a - 1)) - 1)
        cval = new_spot[i] + (z-c)*l/2
        while cval > b - new_spot_sum or cval < 0:
            a = np.random.rand()
            z = np.sign(a - 0.5) * T * ((1 + 1.0 / T) ** (np.abs(2 * a - 1)) - 1)
            cval = new_spot[i] + (z - c) * l / 2
        new_spot[i] += (z - c) * l / 2

        new_spot_sum += new_spot[i]
        c *= l
        l -= new_spot[i] + spot[i]
        c = (c + (new_spot[i] - spot[i])) / l
    return new_spot


def optimize_by_annealing(f, T, specifications, spots_number):
    if spots_number <= 0:
        raise ValueError("Number of spots must be positive")

    cur_spot = np.zeros(f.input_dimension)
    cur_value = f.calculate(cur_spot)
    max_spot = np.zeros(f.input_dimension)
    max_value = cur_value
    for s in range(spots_number):
        new_spot = np.zeros(f.input_dimension)
        for spec in specifications:
            vals = _generate_spot_fast_annealing([cur_spot[i] for i in spec[:-1]], T, spec[-1])
            for j in range(len(spec) - 1):
                new_spot[spec[j]] = vals[j]
        new_value = f.calculate(new_spot)

        h_try = np.random.rand()
        if (cur_value - new_value)/T > 1:
            h = 1
        else:
            h = np.exp(float((cur_value - new_value)/T))
        if new_value > cur_value or h_try >= h:
            cur_spot = new_spot
            cur_value = new_value

            if cur_value > max_value:
                max_spot = cur_spot
                max_value = cur_value
        T = T*np.exp(-0.005)

    return max_spot
