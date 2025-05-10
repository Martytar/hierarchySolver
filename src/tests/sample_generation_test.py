from src.samples.models import TwoLevelModel
from src.samples.sample_generators import generate_random_values_two_level_model, read_from_file
from numpy import random

import os

# попытка генерации двухуровневых моделей с 1-6 игроками второго уровня.
# для каждого случая будут взяты различные комбинации числа ресурсов и продуктов
# содержание модели будет отображено в индексе тестового набора: sample_x_y1_y2_..._yk. числа будут сгенерированы произвольным образом
# в пределах 30 тестовых наборов для каждой модели

# filepath = r"C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\samples\samples_data"
# for i in range(1, 7):
#     for j in range(0, 30):
#
#         resource_type_dim = random.randint(1, 6)
#         product_type_dims = [random.randint(1, 6) for r in range(i)]
#         filpath_addiction = rf'\{i}\sample_{resource_type_dim}'
#         for k in product_type_dims:
#             filpath_addiction += f'_{k}'
#         filpath_addiction += '.txt'
#
#         while os.path.exists(filepath + filpath_addiction):
#
#             resource_type_dim = random.randint(1, 6)
#             product_type_dims = [random.randint(1, 6) for r in range(i)]
#             filpath_addiction = rf'\{i}\sample_{resource_type_dim}'
#             for k in product_type_dims:
#                 filpath_addiction += f'_{k}'
#             filpath_addiction += '.txt'
#
#         model = TwoLevelModel(resource_type_dim, product_type_dims)
#         generate_random_values_two_level_model(model, 1000.0, 1000.0, 1000.0, 1000.0, True)
#         model.write(filepath + filpath_addiction)


# попытка чтения модели с файла

filepath = r"C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\samples\samples_data\6\sample_5_5_1_2_5_4_3.txt"
model = read_from_file(filepath)
model.print()