import copy
import numpy as np


class TwoLevelModel:

    # при инициализации модели двухуровневой игры необходимы:
    # 1)количество типов ресурсов, которыми располагает игрок первого уровня иерархии
    # 1)количества типов продукции каждого из игроков второго уровня
    # На основе этой информации может быть инициализирована пустая модель,
    # для которой могут быть заданы функции выигрыша игроков, а также вектор/матрицы ограничений

    def __init__(self, resource_type_dim, product_type_dims):
        self._resource_type_dim = resource_type_dim
        self._product_type_dims = product_type_dims

        self._resource_limit = np.zeros(resource_type_dim)
        self._restriction_matrices = []

        major_cost_coefs_len = 0
        self._minor_cost_coefs_list = []

        for dim in product_type_dims:
            major_cost_coefs_len += dim
            self._minor_cost_coefs_list.append(np.zeros(dim))
            self._restriction_matrices.append(np.zeros((resource_type_dim, dim)))

        self._major_cost_coefs = np.zeros(major_cost_coefs_len)

    @property
    def resource_type_dim(self):
        return copy.deepcopy(self._resource_type_dim)

    @property
    def product_type_dims(self):
        return copy.deepcopy(self._product_type_dims)

    @property
    def resource_limit(self):
        return copy.deepcopy(self._resource_limit)

    @property
    def restriction_matrices(self):
        return copy.deepcopy(self._restriction_matrices)

    @property
    def minor_cost_coefs_list(self):
        return copy.deepcopy(self._minor_cost_coefs_list)

    @property
    def major_cost_coefs(self):
        return copy.deepcopy(self._major_cost_coefs)

    @resource_limit.setter
    def resource_limit(self, limit):
        if len(self._resource_limit) != len(limit):
            raise ValueError("New Limit must have the same length as previous one!")
        for i in limit:
            if i < 0.0:
                raise ValueError("Limit must contain only non-negative values")

        self._resource_limit = limit

    @restriction_matrices.setter
    def restriction_matrices(self, matrices, indexes=None):

        def is_compatible_matrices(m1, m2):
            if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
                return False
            return True

        def is_non_negative_matrix(m):
            for arr in m:
                for val in arr:
                    if val < 0.0:
                        return False
            return True

        if indexes is None:
            if len(matrices) != len(self._restriction_matrices):
                raise ValueError(
                    "No indexes found, can't set new matrices! Change length of the list or specify indexes")
            else:
                for i in range(len(matrices)):
                    if not is_compatible_matrices(self._restriction_matrices[i], matrices[i]):
                        raise ValueError(f"Incompatible shape of matrix at index {i}")
                    if not is_non_negative_matrix(matrices[i]):
                        raise ValueError(f"Matrix with negative values at index {i}")

                for i in range(len(matrices)):
                    self._restriction_matrices[i] = copy.deepcopy(matrices[i])
        else:
            if len(indexes) != len(matrices):
                raise ValueError("Number of indexes is not equal to number of matrices")
            for i in indexes:
                if i < -1 * len(self._restriction_matrices) or i >= len(self._restriction_matrices):
                    raise ValueError("Indexes out of range")

            for i in len(matrices):
                if not is_compatible_matrices(self._restriction_matrices[indexes[i]], matrices[i]):
                    raise ValueError(f"Incompatible shape of matrix at index {indexes[i]}")
                if not is_non_negative_matrix(matrices[i]):
                    raise ValueError(f"Matrix with negative values at index {indexes[i]}")

            for i in len(matrices):
                self._restriction_matrices[indexes[i]] = copy.deepcopy(matrices[i])

    @minor_cost_coefs_list.setter
    def minor_cost_coefs_list(self, coefs_list, indexes=None):
        if indexes is None:
            if len(self._minor_cost_coefs_list) != len(coefs_list):
                raise ValueError(
                    "Incorrect number of coefs arrays given! Specify indexes or check your coefs list length")
            for i in range(len(coefs_list)):
                if len(self._minor_cost_coefs_list[i]) != len(coefs_list[i]):
                    raise ValueError(f"Incorrect size of coef array at index {i}")
                for j in coefs_list[i]:
                    if j < 0.0:
                        raise ValueError(f"Coef array at index {i} contains negative values")

            self._minor_cost_coefs_list = copy.deepcopy(coefs_list)

        else:
            if len(indexes) != len(coefs_list):
                raise ValueError("Number of indexes is not equal to number of coef arrays")
            for i in indexes:
                if i < -1 * len(self._minor_cost_coefs_list) or i >= len(self._minor_cost_coefs_list):
                    raise ValueError("Indexes out of range")

            for i in range(len(coefs_list)):
                if len(self._minor_cost_coefs_list[indexes[i]]) != len(coefs_list[i]):
                    raise ValueError(f"Incompatible size of coef array at index {indexes[i]}")
                for j in coefs_list[i]:
                    if j < 0.0:
                        raise ValueError(f"Coef array at index {indexes[i]} contains negative values")

            for i in range(len(coefs_list)):
                self._minor_cost_coefs_list[indexes[i]] = copy.copy(coefs_list[i])

    @major_cost_coefs.setter
    def major_cost_coefs(self, coefs):
        if len(self._major_cost_coefs) != len(coefs):
            raise ValueError("Incompatible sizes of lists")
        for i in coefs:
            if i < 0.0:
                raise ValueError("Coefs must not contain negative values")
        self._major_cost_coefs = copy.copy(coefs)

    def print(self):
        print("Двухуровневая иерархическая игра:")
        print("Число игроков второго уровня: ", len(self._restriction_matrices))
        print("Число типов ресурсов: ", self._resource_type_dim)
        print("Число типов продукции каждого игрока: ", self._product_type_dims)
        print("Ценовые коэффициенты игрока первого уровня: ", self._major_cost_coefs)
        print("Ценовые коэффициенты игроков второго уровня:")
        for i in range(len(self._minor_cost_coefs_list)):
            print(f"{i})", self._minor_cost_coefs_list[i])
        print("Матрицы производственных ограничений игроков второго уровня:")
        for i in range(len(self._restriction_matrices)):
            print(f"{i})", self._restriction_matrices[i])

    def write(self, filepath):
        file = open(filepath, 'w')

        file.write(f'{self._resource_type_dim}')
        for i in range(len(self._product_type_dims)):
            file.write(f' {self._product_type_dims[i]}')
        file.write('\n')

        file.write(f'{self._resource_limit[0]}')
        for i in range(1, len(self._resource_limit)):
            file.write(f' {self.resource_limit[i]}')
        file.write('\n')

        file.write(f'{self._major_cost_coefs[0]}')
        for i in range(1, len(self._major_cost_coefs)):
            file.write(f' {self._major_cost_coefs[i]}')
        file.write('\n')

        for i in range(len(self._minor_cost_coefs_list)):
            file.write(f'{self._minor_cost_coefs_list[i][0]}')
            for j in range(1, len(self._minor_cost_coefs_list[i])):
                file.write(f' {self._minor_cost_coefs_list[i][j]}')
            file.write('\n')

        for i in range(len(self._restriction_matrices)):
            matrix = self._restriction_matrices[i]

            for j in range(len(matrix)):
                file.write(f'{matrix[j][0]}')
                for k in range(1, len(matrix[j])):
                    file.write(f' {matrix[j][k]}')
                file.write('\n')

        file.close()