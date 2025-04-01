from functions import TreeFunction
from simplex_solving_methods import solve_simplex
import sympy as sp
import numpy as np

def run_main():
    print('program is running')

    k = 3
    n = 2

    c2 = (322, 279)
    A2 = [[15, 31], [49, 14], [25, 8]]

    u2 = np.array([])  # переменные, которые мы будем варьировать для второго завода
    for i in range(k+1, 2*k+1):
        u2 = np.append(u2, [sp.Symbol(f'u_{i}')])

    f = solve_simplex(c2, A2, u2, True)

    print(f.calculate((100, 25, 25)))

if __name__ == '__main__':
    run_main()

