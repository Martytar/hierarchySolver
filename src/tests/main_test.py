from src.hierarchySolver.optimisation_methods import optimize_by_monte_carlo
from src.hierarchySolver.functions import LinearCombinationFunction
from src.hierarchySolver.simplex_solving_methods import solve_simplex
from verifiers import *
import sympy as sp
import numpy as np

k = 3
n1 = 4
n2 = 2
b = (412, 940, 313)

a1 = [434, 273, 312, 433]
c1 = (425, 306, 67, 155)

A1 = [[17, 37, 46, 50], [3, 18, 45, 40], [34, 43, 18, 48]]

a2 = [331, 412]
c2 = (322, 279)
A2 = [[15, 31], [49, 14], [25, 8]]

u1 = np.array([])  # переменные, которые мы будем варьировать для первого завода
for i in range(1, k + 1):
    u1 = np.append(u1, [sp.Symbol(f'u_{i}')])

u2 = np.array([])  # переменные, которые мы будем варьировать для второго завода
for i in range(k+1, 2*k+1):
    u2 = np.append(u2, [sp.Symbol(f'u_{i}')])

f1 = solve_simplex(a1, A1, u1, True)
f2 = solve_simplex(a2, A2, u2, True)

print(f1.input_dimension, f1.output_dimension)
print(f2.input_dimension, f2.output_dimension)

rf = LinearCombinationFunction(np.array(np.concatenate((c1, c2), 0)), [f1, f2])
optimal_spot = optimize_by_monte_carlo(rf, ((0, 3, 412), (1, 4, 940), (2, 5, 313)), 100)
print(optimal_spot)
print(rf.calculate(optimal_spot))

print("Is solution appropriate: ", is_appropriate_solution(optimal_spot, b, [f1, f2], [A1, A2], subs=1))

print(rf.calculate([363.44980828, 456.2013237, 283.50334995, 38.14198095, 250.85900044, 24.83128383]))
print(np.matmul(a1, f1.calculate([363.44980828, 456.2013237, 283.50334995])))
print(np.matmul(a2, f2.calculate([38.14198095, 250.85900044, 24.83128383])))