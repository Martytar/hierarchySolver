import copy

import numpy as np
import sympy as sp
from src.hierarchySolver.functions import TreeFunction
from scipy.optimize import linprog
from sympy import symbols, Poly, Eq, Add

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

def _solveTableWithParameter(table, evaluation, basis, currentNode, restricts, basis_memory = [], pair=[]):

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
            if currentNode.related_tree_function.output_dimension is None:
                currentNode.related_tree_function.output_dimension = len(currentNode.expression)
            return

        # находим множество строк, подозрительных на ведущую строку
        potentRow = []
        for i in range(0, len(tab)):
            if tab[i, c] > 0:
                potentRow = np.append(potentRow, i)

        evals = []
        for i in potentRow:
            evals.append(tab[int(i), 0] / tab[int(i), c])


        #проверка целостности ветви. Если ветвь отрезана от дерева, то дальнейшее ветвление прекращается
        primary_node = currentNode
        while primary_node != currentNode.related_tree_function.primaryNode:
            primary_node = primary_node.parent_node
            if primary_node == None:
                return

        for i in range(len(potentRow)):

            new_restricts = np.copy(restricts)
            for j in range(len(potentRow)):
                if i != j:
                    new_restricts = np.append(new_restricts, evals[i] - evals[j])

            if True: #is_system_feasible(new_restricts, currentNode.related_tree_function.variables):

                nextEval = evals[i]
                nextNode = TreeFunction.Node(nextEval,
                                             related_tree_function=currentNode.related_tree_function,
                                             parent_node=currentNode)
                currentNode.links.append(nextNode)
                _solveTableWithParameter(tab, nextEval, base, nextNode, new_restricts, basis_memory, [potentRow[i], c])

            else:
                return
    else:
        # если заданы ведущие строка и столбец, преобразуем таблицу и заново запустим метод рекурсивно

        base[int(pair[0])] = pair[1]

        for b in basis_memory:
            basis_sample = b[0]

            is_same_basis = True
            for i in range(len(base)):
                if base[i] != basis_sample[i]:
                    is_same_basis = False
                    break
            if is_same_basis:
                basis_parent_node = b[1]
                basis_identifying_eval = b[2]
                for link in basis_parent_node.links:
                    if link.evaluation == basis_identifying_eval:
                        link.parent_node = None
                        basis_parent_node.links.remove(link)
                        break

                return

        tab[int(pair[0]), :] /= tab[int(pair[0]), int(pair[1])]
        for i in range(0, len(tab)):
            if i != pair[0]:
                tab[i, :] -= tab[int(pair[0]), :] * tab[i, int(pair[1])]

        extended_basis_memory = copy.copy(basis_memory)
        extended_basis_memory.append([copy.copy(base), currentNode.parent_node, eval])

        _solveTableWithParameter(tab, eval, base, currentNode, restricts, extended_basis_memory)

def solve_simplex_recursion(c, A, u, parametric=False):
    if parametric:
        rest = np.array([])
        tab = _makeTable(c, A, u)
        n = len(A[0])
        m = len(A)
        basis = [n+i for i in range(1, m+1)]

        f = TreeFunction(u, TreeFunction.Node())
        _solveTableWithParameter(tab, rest, basis, f.primaryNode, [])
        return f
    else:
        raise ValueError("Non-parametric method isn't ready yet")

def solve_simplex_stack(c, A, u, parametric=False):
    if parametric:
        tab = _makeTable(c, A, u)
        m = len(A)
        basis = [len(A[0]) + i + 1 for i in range(m)]  # Базисные переменные

        # Создаем корневую ноду дерева
        f = TreeFunction(u, TreeFunction.Node())
        stack = [(tab, basis, f.primaryNode, [])]  # Стек: (таблица, базис, нода, ведущая пара)

        while stack:
            current_tab, current_basis, current_node, pair = stack.pop()

            if not pair:
                # Фаза выбора ведущего столбца и строк
                leading_col = None
                # Ищем ведущий столбец (минимальный отрицательный в последней строке)
                min_val = 0
                for j in range(1, len(current_tab[0])):
                    if current_tab[-1, j] < min_val:
                        min_val = current_tab[-1, j]
                        leading_col = j

                if leading_col is None:
                    # Нет отрицательных коэффициентов - решение найдено
                    current_node.expression = _getExpressionFromTable(current_tab, current_basis)
                    if current_node.related_tree_function.output_dimension is None:
                        current_node.related_tree_function.output_dimension = len(current_node.expression)
                    continue

                # Находим потенциальные ведущие строки
                potential_rows = []
                for i in range(len(current_tab) - 1):  # Исключаем последнюю строку (целевую)
                    if current_tab[i, leading_col] > 0:
                        potential_rows.append(i)

                # Обрабатываем строки в обратном порядке для корректного порядка в дереве
                for row in reversed(potential_rows):
                    next_eval = current_tab[row, 0] / current_tab[row, leading_col]
                    next_node = TreeFunction.Node(next_eval, related_tree_function=current_node.related_tree_function)
                    current_node.links.append(next_node)
                    # Добавляем в стек с указанием ведущей пары
                    stack.append((np.copy(current_tab), np.copy(current_basis), next_node, [row, leading_col]))
            else:
                # Фаза преобразования таблицы
                row, col = pair
                # Копируем таблицу и базис для модификации
                new_tab = np.copy(current_tab)
                new_basis = np.copy(current_basis)

                # Нормализуем ведущую строку
                pivot = new_tab[row, col]
                new_tab[row, :] /= pivot

                # Обновляем остальные строки
                for i in range(len(new_tab)):
                    if i != row:
                        new_tab[i, :] -= new_tab[row, :] * new_tab[i, col]

                # Обновляем базис
                new_basis[row] = col

                # Добавляем в стек для дальнейшей обработки (без ведущей пары)
                stack.append((new_tab, new_basis, current_node, []))

        return f
    else:
        raise ValueError("Non-parametric method isn't ready yet")

def is_system_feasible(expressions, variables):

    # Создаем словарь для замены переменных на числовые индексы
    var_to_index = {var: i for i, var in enumerate(variables)}
    num_vars = len(variables)

    # Искусственная переменная t добавляется в конец
    t_index = num_vars

    # Матрица коэффициентов A и вектор b для условий вида A @ [x1, x2, ..., t] <= b
    A = []
    b = []

    for expr in expressions:
        # Преобразуем выражение к виду expr <= 0 (если это не так, измените знак)
        # Здесь предполагается, что выражения уже имеют вид expr <= 0
        coeffs = []

        # Коэффициенты при переменных
        for var in variables:
            coeff = expr.coeff(var)
            coeffs.append(float(coeff))

        # Коэффициент при t (добавляется в правую часть как +t)
        coeffs.append(1.0)  # expr <= t → expr - t <= 0

        A.append(coeffs)
        b.append(0.0)  # Переносим правую часть в левую

    # Целевая функция: минимизировать t (последняя переменная)
    c = np.zeros(num_vars + 1)
    c[t_index] = 1.0  # min t

    # Ограничения: A @ [x1, ..., xn, t] <= b
    A_ub = np.array(A)
    b_ub = np.array(b)

    # Границы переменных: x_i >= 0, t >= 0
    bounds = [(0, None) for _ in range(num_vars + 1)]

    # Решаем задачу ЛП
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    # Если задача решена успешно и t <= 0 (с учетом численной погрешности), система совместна
    if result.success:
        return result.x[t_index] <= 1e-8  # Учет погрешности вычислений
    else:
        return False  # Если задача нерешаема (например, неограничена), система несовместна

def printTable(table):
    for i in range(len(table)):
        for j in range(len(table[0])):
            if type(table[i][j]) == float:
                print(np.round(table[i][j], 2), end='  ')
            else:
                print(table[i][j], end='  ')
        print()
    print()