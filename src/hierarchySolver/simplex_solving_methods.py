import numpy as np
import sympy as sp
from functions import TreeFunction

#Тут располагаются методы для решения симплексных таблиц (с параметром и без)


def _makeTable(c, A, u):  # компановка симплексной таблицы по исходным данным

    # c - вектор коэфф-в целевой функции
    # A - матрица весовых к-в для ограничений (1 строка = 1 ограничение)
    # u - вектор верхних границ ограничений

    c = np.array(c)
    zer = np.diag(np.diag(np.ones((len(A), len(A)))))
    z = np.append(np.append([0], [-1 * c]), np.zeros(len(A)))
    tab = np.row_stack((np.column_stack((u, A, zer)), z))

    return tab

def _getExpressionFromTable(tab, basis):
    n = len(tab[0, :]) - len(tab)
    exp = sp.Matrix(np.zeros(n))
    for i in range(0, len(basis)):
        if basis[i] <= n:
            exp[basis[i]-1] = tab[i, 0]
    return exp

def _solveTableWithParameter(table, evaluation, basis, currentNode, pair = []):

    # table -текущая симплексная таблица
    # restricts - текущие ограничения на параметры
    # basis - индексы базисных переменных

    tab = np.copy(table)
    eval = np.copy(evaluation)
    base = np.copy(basis)

    if not pair:
        # выбираем ведущий столбец
        c = 1
        for i in range(1, len(tab[0])):
            if tab[-1, i] < tab[-1, c]:
                c = i
        if tab[-1, c] >= 0:
            currentNode.expression = _getExpressionFromTable(tab, base)
            return

        # находим множество строк, подозрительных на ведущую строку
        potentRow = []
        for i in range(0, len(tab)):
            if tab[i, c] > 0:
                potentRow = np.append(potentRow, i)

        for i in potentRow:
            nextEval = tab[int(i), 0] / tab[int(i), c]
            nextNode = TreeFunction.Node(nextEval)
            currentNode.links.append(nextNode)
            _solveTableWithParameter(tab, nextEval, base, nextNode, [i, c])
    else:
        # если заданы ведущие строка и столбец, преобразуем таблицу и заново запустим метод рекурсивно
        tab[int(pair[0]), :] /= tab[int(pair[0]), int(pair[1])]
        for i in range(0, len(tab)):
            if i != pair[0]:
                tab[i, :] -= tab[int(pair[0]), :] * tab[i, int(pair[1])]

        base[int(pair[0])] = pair[1]
        _solveTableWithParameter(tab, eval, base, currentNode)

def solve_simplex(c, A, u, parametric=False):
    if parametric:
        rest = np.array([])
        tab = _makeTable(c, A, u)
        n = len(A[0])
        m = len(A)
        basis = [n+i for i in range(1, m+1)]

        f = TreeFunction(u, TreeFunction.Node())
        _solveTableWithParameter(tab, rest, basis, f.primaryNode)
        return f

