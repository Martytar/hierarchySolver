from optimisation_methods import optimize_by_monte_carlo
from optimisation_methods import optimize_by_annealing
from functions import LinearCombinationFunction
from simplex_solving_methods import solve_simplex_recursion
from src.tests.verifiers import is_appropriate_solution

from src.samples.sample_generators import read_from_file
from src.samples.models import TwoLevelModel
from src.hierarchySolver.estimation_methods import *
import sympy as sp
import numpy as np
import sys

def run_main():
    print('program is running')

    save_filepath = r'C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\estimation_data'
    sample_filepath = r'C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\samples\statistical_estimation_samples_data\1'

    sys.setrecursionlimit(3000)
    for i in range(5, 6):
        for j in range(6, 7):

            save_file = open(save_filepath + rf'\{i}_{j}_stats.txt', 'a')

            u = np.array([])
            for i in range(1, i + 1):
                u = np.append(u, [sp.Symbol(f'u_{i}')])

            for k in range(1, 100):
                model = read_from_file(sample_filepath + rf'\{i}_{j}_num{k}.txt')
                with timer() as t:
                    f = solve_simplex_recursion(model.minor_cost_coefs_list[0], model.restriction_matrices[0], u, True)

                time = t()
                depth, total = bfs(f.primaryNode)
                save_file.write(f'{time} {depth} {total}\n')
                print(f"Test {k} finished! depth:{depth} total:{total}")

            save_file.close()
    sys.setrecursionlimit(1000)
    print('program finished')


if __name__ == '__main__':
    run_main()

