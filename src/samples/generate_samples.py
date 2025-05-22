from src.hierarchySolver.models import TwoLevelModel
from src.samples.sample_generators import generate_random_values_two_level_model


#скрипт для генерации тестовых моделей для оценки эффективности работы парметрического симплекс-метода
filepath = r"C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\samples\statistical_estimation_samples_data\1"
for i in range(1,11):
    for j in range(1, 11):
        model = TwoLevelModel(i, [j])
        for k in range(100):
            generate_random_values_two_level_model(model, 1000.0, 1000.0, 1000.0, 1000.0, True)
            filepath_addiction = rf'\{i}_{j}_num{k}.txt'
            model.write(filepath + filepath_addiction)