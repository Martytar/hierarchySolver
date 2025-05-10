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


def print_difference_solution_level_1(strategy, b):
    dim = len(b)
    if len(strategy) % dim != 0:
        raise ValueError("Incorrect size of strategy")
    iters = int(len(strategy) / dim)

    sum = np.zeros(dim)
    for i in range(iters):
        sub_strategy = strategy[dim * i:dim * (i + 1)]
        for j in range(len(sub_strategy)):
            sum[j] += sub_strategy[j]

    difference = []
    for i in range(dim):
        difference.append(b[i] - sum[i])
    return


def is_appropriate_solution_level_2(strategy, A, u):

    resources = np.matmul(A, strategy)
    for i in range(len(resources)):
        if resources[i] > u[i]:
            return False

    return True


def print_difference_solution_level_2(strategy, A, u):

    resources = np.matmul(A, strategy)
    difference = []
    for i in range(len(resources)):
        difference.append(u[i] - resources[i])

    print(difference)
    return


def is_appropriate_solution(strategy_u, b, strategies_f, matrices, subs=0):

    appropriation_flag = True

    if not is_appropriate_solution_level_1(strategy_u, b):
        print('U_strategy is not appropriate')

        if subs>0:
            print("The difference array of level 1 solution and b:")
            print_difference_solution_level_1(strategy_u, b)

        appropriation_flag = False

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
            print(f"V_strategy is not appropriate, code: {i+1}")
            print(np.matmul(matrix, f.calculate(sub_strategy_u)), sub_strategy_u)

            if subs>0:
                print("The difference array of level 1 solution with donated resources (U):")
                print_difference_solution_level_2(f.calculate(sub_strategy_u), matrix, sub_strategy_u)

            appropriation_flag = False

    return appropriation_flag
