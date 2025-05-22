import numpy.random as random
from src.hierarchySolver.models import TwoLevelModel

def generate_random_values_two_level_model(model, resource_limit, major_cost_limit, restriction_matrices_limit, minor_cost_limit, is_int_type = False):

    #borders - кортеж из 1 элементов (границы генерации)
    def get_random(borders):
        number = 0
        if is_int_type:
            number = random.randint(int(borders[0]), int(borders[1]))
        else:
            number = random.rand()*(borders[1] - borders[0]) + borders[0]
        return number

    model.resource_limit = [get_random([0, resource_limit]) for i in range(len(model.resource_limit))]

    model.major_cost_coefs = [get_random([0, major_cost_limit]) for i in range(len(model.major_cost_coefs))]

    matrices = model.restriction_matrices
    for m in matrices:
        for i in range(len(m)):
            for j in range(len(m[0])):
                m[i][j] = get_random([0, restriction_matrices_limit])

    model.restriction_matrices = matrices

    minors = model.minor_cost_coefs_list
    for i in range(len(minors)):
        for j in range(len(minors[i])):
            minors[i][j] = get_random([0, minor_cost_limit])

    model.minor_cost_coefs_list = minors

def read_from_file(filename):
    file = open(filename, 'r')

    resource_product_dims = list(map(int, file.readline().split(' ')))

    resource_dim = resource_product_dims[0]
    product_dims = resource_product_dims[1:]

    resource_limit = list(map(float, file.readline().split(' ')))

    major_cost_coefs = list(map(float, file.readline().split(' ')))

    minor_cost_coefs_list = []
    for i in range(len(product_dims)):
        minor_cost_coefs = list(map(float, file.readline().split(' ')))
        minor_cost_coefs_list.append(minor_cost_coefs)

    restriction_matrices = []
    for i in range(len(product_dims)):
        matrix = []
        for j in range(resource_dim):
            matrix.append(list(map(float, file.readline().split(' '))))
        restriction_matrices.append(matrix)

    model = TwoLevelModel(resource_dim, product_dims)
    model.resource_limit = resource_limit
    model.major_cost_coefs = major_cost_coefs
    model.minor_cost_coefs_list = minor_cost_coefs_list
    model.restriction_matrices = restriction_matrices

    return model
