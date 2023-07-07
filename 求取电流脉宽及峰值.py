import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# 读取folder_path里的所有csv文件,将处理结果输出到 out_folder
folder_path = r'D:\03  实验数据\电压电流随气压变化\15pa\test数据预处理'  # 待处理文件夹路径
output_folder = r'D:\03  实验数据\电压电流随气压变化\15pa\test数据预处理\电流'  # 输出文件夹路径
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# 获取指定文件夹内所有 csv 文件的文件名
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]




res = []       #这只是一个空集，不需要管也不要删

for csv_file in csv_files:

    # 设置各种参数（需要根据数据情况做出更改）
    # step_size = 0.1      # 设置步长：数据点之间的时间间隔(采样率的倒数)单位是微秒
    #time_lower_bound_pd1 = 20  #选取光电流的一部分来做处理（找峰值，归一化）  下限                 ！！！！！应该改
    #time_upper_bound_pd1 = 60 #上限                                                         ！！！！！改
    time_lower_bound = -50
    time_upper_bound = 1000


    # 读取数据
    with open(os.path.join(folder_path, csv_file), 'r') as input_file:

        df = pd.read_csv(os.path.join(folder_path, csv_file))
        time = df.iloc[:, 0].astype(float)
        current =df.iloc[:, 1].astype(float)
        voltage = df.iloc[:, 4].astype(float)

        # 计算平均幅值并减去平均值
        current_average = np.mean(current[:100])
        voltage_average = np.mean(voltage[:100])
        current -= current_average
        voltage -= voltage_average

        # 计算电流起始点和终止点、峰值点
        #time_zero_index = np.argmin(np.abs(time))
        current_peak_index = np.argmax(np.abs(current))
        current_peak_value = current[current_peak_index]
        current_peak = pd.Series([current_peak_value],index= [current_peak_index])

        current_ori_dot = []  # 将峰值点之后的第一个小于0.1的点作为电流的中止点
        time_range_indices1 = np.where((time <= time[current_peak_index]) & (time >= time_lower_bound))[0]
        time_range_values1 = time[time_range_indices1]
        time_range1 = pd.Series(time_range_values1, index=time_range_indices1)
        for i in time_range_indices1:
            if np.abs(current[i]) < 0.05 * abs(current_peak_value):
                current_ori_dot.append(i)
        current_ori_index = np.max(current_ori_dot)
        current_ori_value = current[current_ori_index]
        current_ori = pd.Series([current_ori_value], index=[current_ori_index])

        current_ter_dot = [] #将峰值点之后的第一个小于0.1的点作为电流的中止点
        time_range_indices2 = np.where((time >= time[current_peak_index]) & (time <= time_upper_bound))[0]
        time_range_values2 = time[time_range_indices2]
        time_range2 = pd.Series(time_range_values2, index=time_range_indices2)
        for i in time_range_indices2:
            if np.abs(current[i]) < 0.05 * abs(current_peak_value):
                current_ter_dot.append(i)
        current_ter_index = np.min(current_ter_dot)
        current_ter_value = current[current_ter_index]
        current_ter = pd.Series([current_ter_value],index = [current_ter_index])

        # 作图
        plt.plot(current, color='black', label='pd1')
        #plt.plot(pd2, color='gray', label='pd2')
        # plt.plot(pd1_peak, color='red', label='pd1_peak', marker='s', markersize=2)
        # plt.plot(pd2_peak, color='blue', label='pd2_peak', marker='s', markersize=2)
        plt.plot(current_ori, color='green', label='pd1_peak', marker='s', markersize=3)
        plt.plot(current_ter, color='blue', label='pd2_peak', marker='s', markersize=3)
        plt.plot(current_peak, color='red', label='pd2_peak', marker='s', markersize=3)

        plt.legend()
        plt.xlabel('Index')
        plt.ylabel('real Values')
        plt.title('current')
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_file))[0] + '.png')
        plt.savefig(output_file)
        plt.close()

        #这里是需要保存的数据
        new_row = [csv_file.split('.csv')[0] , current_peak_value , time[current_peak_index]-time[current_ori_index],
                   time[current_ori_index] , time[current_ter_index] ,time[current_ter_index]-time[current_ori_index] ]
        res.append(new_row)

with open(os.path.join(output_folder, os.path.basename(folder_path) + '_pd_res.csv'), 'w',
          newline='') as output_file:
    csv_writer = csv.writer(output_file)
    for row in res:
        csv_writer.writerow(row)

print('done')






