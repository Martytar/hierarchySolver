from src.hierarchySolver.models import TwoLevelModel
from src.samples.sample_generators import generate_random_values_two_level_model
from src.hierarchySolver.functions import LinearCombinationFunction
from src.hierarchySolver.simplex_solving_methods import solve_simplex_recursion
from src.hierarchySolver.estimation_methods import timer
from src.hierarchySolver.optimisation_methods import optimize_by_monte_carlo, optimize_by_annealing
import numpy as np
import sympy as sp


for i in range(8, 9):
    #################################################################################################################
    model = TwoLevelModel(i, [3, 2])
    generate_random_values_two_level_model(model, 1000.0, 1000.0, 1000.0, 1000.0, True)

    u = np.array([])
    for j in range(1, i+1):
        u = np.append(u, [sp.Symbol(f'u_{j}')])

    funs = []
    for j in range(2):
        funs.append(solve_simplex_recursion(model.minor_cost_coefs_list[j], model.restriction_matrices[j], u, True))

    target_f = LinearCombinationFunction(model.major_cost_coefs, funs)

    print(f'Modelling {i} is done')
    #################################################################################################################
    iters = [500*k for k in range(1, 9)]

    file = open(rf'C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\estimation_data\annealing_{i}.txt', 'w')
    anneal_samples = []
    for iter in iters:

        with timer() as t:
            r_annealing = optimize_by_annealing(target_f, 100, [(k, k+i, model.resource_limit[k]) for k in range(i)], iter)
        time = t()
        file.write(str([time, target_f.calculate(r_annealing)]))
        file.write('\n')
    file.close()
