from src.hierarchySolver.models import TwoLevelModel
from src.samples.sample_generators import generate_random_values_two_level_model
from src.hierarchySolver.functions import LinearCombinationFunction
from src.hierarchySolver.simplex_solving_methods import solve_simplex_recursion
from src.hierarchySolver.estimation_methods import timer
from src.hierarchySolver.optimisation_methods import optimize_by_monte_carlo, optimize_by_annealing
import numpy as np
import sympy as sp


#################################################################################################################
model = TwoLevelModel(3, [3, 3])
generate_random_values_two_level_model(model, 1000.0, 1000.0, 1000.0, 1000.0, True)

u = np.array([])
for i in range(1, 4):
    u = np.append(u, [sp.Symbol(f'u_{i}')])

funs = []
for i in range(2):
    funs.append(solve_simplex_recursion(model.minor_cost_coefs_list[i], model.restriction_matrices[i], u, True))

target_f = LinearCombinationFunction(model.major_cost_coefs, funs)

print('Modelling is done')
#################################################################################################################

iter_set = [500*k for k in range(1, 16)]

monte_samples = []
annealing_samples = []

for iter in iter_set:

    with timer() as t:
        r_monte = optimize_by_monte_carlo(target_f, [(0, 3, model.resource_limit[0]),
                                                     (1, 4, model.resource_limit[1]),
                                                     (2, 5, model.resource_limit[2])], iter)
    time = t()

    monte_samples.append((time, target_f.calculate(r_monte)))


    with timer() as t:
        r_annealing = optimize_by_annealing(target_f, 100, [(0, 3, model.resource_limit[0]),
                                                            (1, 4, model.resource_limit[1]),
                                                            (2, 5, model.resource_limit[2])], iter)
    time = t()

    annealing_samples.append((time, target_f.calculate(r_annealing)))
    print('gotcha!')

print(str(monte_samples))
print(str(annealing_samples))

file = open(rf'C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\estimation_data\annealing_4_4_4_4.txt', 'a')
file.write('\n')
file.write('\n')
file.write(str(monte_samples))
file.write('\n')
file.write(str(annealing_samples))
file.close()