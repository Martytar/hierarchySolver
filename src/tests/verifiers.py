import numpy as np


def is_appropriate_solution_level_1(strategy, b):
    dim = len(b)
    if len(strategy) % dim != 0:
        raise ValueError("Incorrect size of strategy")
    iters = int(len(strategy)/dim)

    sum = np.zeros(dim)
    for i in range(iters):
        sub_strategy = strategy[dim*i:dim*(i+1)]
        for j in range(len(sub_strategy)):
            sum[j] += sub_strategy[j]
    for i in range(dim):
        if sum[i] > b[i]:
            return False

    return True


def is_appropriate_solution_level_2(strategy, A, u):

    resources = np.matmul(A, strategy)
    for i in range(len(resources)):
        if resources[i] > u[i]:
            return False

    return True


def is_appropriate_solution(strategy_u, b, strategies_f, matrices):

    if not is_appropriate_solution_level_1(strategy_u, b):
        return False

    dim = len(b)
    if len(strategy_u) % dim != 0:
        raise ValueError("Incorrect size of strategy_u")
    iters = int(len(strategy_u)/dim)
    if iters != len(strategies_f) or iters != len(matrices):
        raise ValueError("Incorrect size of strategies_f/matrices")

    for i in range(iters):
        sub_strategy_u = strategy_u[dim*i:dim*(i+1)]
        f = strategies_f[i]
        matrix = matrices[i]
        if not is_appropriate_solution_level_2(f.calculate(sub_strategy_u), matrix, sub_strategy_u):
            return False

    return True