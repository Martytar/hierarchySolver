import os
import numpy as np
from matplotlib import pyplot as plt


time = []
depth = []
total = []

average_time = []
max_time = []
min_time = []

average_depth = []
max_depth = []
min_depth = []

average_total = []
max_total = []
min_total = []

samples_num = []

for i in range(2, 14):

    av_t, max_t, min_t = 0.0, 0.0, 10000000.0
    av_d, max_d, min_d = 0.0, 0.0, 10000000.0
    av_tot, max_tot, min_tot = 0.0, 0.0, 10000000.0
    s_num = 0

    ctime = []
    cdepth = []
    ctotal = []

    for j in range(1, i):
        if os.path.exists(rf'C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\estimation_data\{j}_{i-j}_stats.txt'):
            cfile = open(rf'C:\Users\АДМИН\PycharmProjects\hierarchySolver\src\estimation_data\{j}_{i-j}_stats.txt')


            lines = cfile.readlines()
            for line in lines:
                vals = list(map(float, line[:-1].split(' ')))


                ctime.append(vals[0])
                cdepth.append(vals[1])
                ctotal.append(vals[2])

                s_num += 1
                av_t += vals[0]
                av_d += vals[1]
                av_tot += vals[2]

                if vals[0] > max_t:
                    max_t = vals[0]
                if vals[1] > max_d:
                    max_d = vals[1]
                if vals[2] > max_tot:
                    max_tot = vals[2]

                if vals[0] < min_t:
                    min_t = vals[0]
                if vals[1] < min_d:
                    min_d = vals[1]
                if vals[2] < min_tot:
                    min_tot = vals[2]

            cfile.close()

    time.append(np.sort(ctime))
    depth.append(np.sort(cdepth))
    total.append(np.sort(ctotal))

    av_t /= s_num
    av_d /= s_num
    av_tot /= s_num

    samples_num.append(s_num)

    average_time.append(av_t)
    average_depth.append(av_d)
    average_total.append(av_tot)

    max_time.append(max_t)
    max_depth.append(max_d)
    max_total.append(max_tot)

    min_time.append(min_t)
    min_depth.append(min_d)
    min_total.append(min_tot)


#считаем квартили времени, глубины и общего количества узлов
time_procentiles = [[time[i][int(k*0.25*len(time[i])) - 1] for k in range(1,5)] for i in range(12)]
depth_procentiles = [[depth[i][int(k*0.25*len(depth[i])) - 1] for k in range(1,5)] for i in range(12)]
total_procentiles = [[total[i][int(k*0.25*len(total[i])) - 1] for k in range(1,5)] for i in range(12)]

time_outs = []
depth_outs = []
total_outs = []



#высчитаем процентное количество выбросов по методике IQR
for i in range(12):
    time_out = 0
    depth_out = 0
    total_out = 0

    for j in time[i]:
        if j > time_procentiles[i][2] + 1.5*(time_procentiles[i][2] - time_procentiles[i][0]):
            time_out += 1
    time_outs.append(time_out / len(time[i]))

    for j in depth[i]:
        if j > depth_procentiles[i][2] + 1.5*(depth_procentiles[i][2] - depth_procentiles[i][0]):
            depth_out += 1
    depth_outs.append(depth_out / len(depth[i]))

    for j in total[i]:
        if j > total_procentiles[i][2] + 1.5*(total_procentiles[i][2] - total_procentiles[i][0]):
            total_out += 1
    total_outs.append(total_out / len(total[i]))


###########################################################################################
x = [i for i in range(2, 14)]
plt.plot(x, time_outs, label='максимальное число узлов', linestyle='-', linewidth=2, color='blue')
plt.plot(x, depth_outs, label='среднее число узлов', linestyle='-', linewidth=2, color='red')
plt.plot(x, total_outs, label='минимальное число узлов', linestyle='-', linewidth=2, color='green')

# Настраиваем график
plt.xlabel('Общеее количество переменных (n)', fontsize=12)
plt.ylabel('число узлов (k)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(np.arange(0, 14, 2))

# Показываем график
plt.tight_layout()
plt.show()