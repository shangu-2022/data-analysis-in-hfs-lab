"""
本数据用来做单路数据的预处理
分为几个部分：
            1. 对数据做初步处理（将时间* 10^6，将电流*98.96367279，两列光电流不动，电压*-1000
            2. 将每一发数据都单独存放，并将时间归零
"""

# 导包
import os
import pandas as pd
import csv
import numpy as np

# 读取folder_path里的所有csv文件,将处理结果输出到 out_folder
folder_path = r'D:\03  实验数据\绝缘件对等离子体参数的影响\绝缘件二\光电流\test'  # 文件夹路径
output_folder = r'D:\03  实验数据\绝缘件对等离子体参数的影响\绝缘件二\光电流\test\数据预处理'  # 输出文件夹路径
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# 获取指定文件夹内所有 csv 文件的文件名
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

for csv_file in csv_files:
    with open(os.path.join(folder_path, csv_file), 'r') as input_file:
        # 读取 csv 文件
        csv_reader = csv.reader(input_file)

        # 跳过前 100 行数据
        for _ in range(100):
            next(csv_reader)

         # 创建空列表用于储存筛选后的数据
        filtered_data_1 = []
        # 遍历剩余行数的数据
        for row in csv_reader:
            # 如果该行数据不足 5 个，则跳过此行数据
            if len(row) < 5:
                continue
            # 将第一列数据乘以 1e6，并将第二、第三列数据乘以相应的系数
            new_row = [float(row[0]) * 1e6, float(row[1]) * 98.96367279, row[2], row[3], float(row[4]) * 1e3, ]
            # 添加处理后的数据到 filtered_data_1 列表中
            filtered_data_1.append(new_row)

    # 将数据拆分开，每一发都写入新的文件。
    with open(os.path.join(output_folder, csv_file.split('.csv')[0] + '_shot1.csv'), 'w', newline='') as output_file_1:
        csv_writer_1 = csv.writer(output_file_1)
        # 写入表头
        # csv_writer_1.writerow(['Time', 'Current', 'Voltage', 'Photodiode1', 'Phododiode2'])
        # 写入数据
        for row in filtered_data_1:
            if -500 <= row[0] <= 1500:
                csv_writer_1.writerow(row)

    with open(os.path.join(output_folder, csv_file.split('.csv')[0] + '_shot2.csv'), 'w', newline='') as output_file_2:
        csv_writer_2 = csv.writer(output_file_2)
        # 写入表头
        # csv_writer_2.writerow(['Time', 'Current', 'Voltage', 'Photodiode1', 'Phododiode2'])
        # 写入数据
        for row in filtered_data_1:
            if 19500 <= row[0] <= 21500:
                row[0] -= 20000
                csv_writer_2.writerow(row)

    with open(os.path.join(output_folder, csv_file.split('.csv')[0] + '_shot3.csv'), 'w', newline='') as output_file_3:
        csv_writer_3 = csv.writer(output_file_3)
        # 写入表头
        # csv_writer_3.writerow(['Time', 'Current', 'Voltage', 'Photodiode1', 'Phododiode2'])
        # 写入数据
        for row in filtered_data_1:
            if 39500 <= row[0] <= 41500:
                row[0] -= 40000
                csv_writer_3.writerow(row)

    with open(os.path.join(output_folder, csv_file.split('.csv')[0] + '_shot4.csv'), 'w', newline='') as output_file_4:
        csv_writer_4= csv.writer(output_file_4)
        # 写入表头
        # csv_writer_4.writerow(['Time', 'Current', 'Voltage', 'Photodiode1', 'Phododiode2'])
        # 写入数据
        for row in filtered_data_1:
            if 59500 <= row[0] <= 61500:
                row[0] -= 60000
                csv_writer_4.writerow(row)

    with open(os.path.join(output_folder, csv_file.split('.csv')[0] + '_shot5.csv'), 'w', newline='') as output_file_5:
        csv_writer_5= csv.writer(output_file_5)
        # 写入表头
        # csv_writer_5.writerow(['Time', 'Current', 'Voltage', 'Photodiode1', 'Phododiode2'])
        # 写入数据
        for row in filtered_data_1:
            if 79500 <= row[0] <= 81500:
                row[0] -= 80000
                csv_writer_2.writerow(row)

print("done!")