"""
十路示波器数据预处理
1. 时间换成微秒；电流乘标定系数；光电流不做处理；电压乘转换系数
2.将5shot分别存放一个csv文件，并且时间归零

"""


# 导入必要的库
import os
import csv

# 输入和输出文件夹路径
folder_path = r'D:\03  实验数据\正式实验\电压电流光电流\十路\20230703\110Pa'
output_folder = r'D:\03  实验数据\正式实验\电压电流光电流\十路\20230703\110Pa\数据预处理'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 定义时间偏移量和发射次数
time_offsets = [0, 200000, 400000, 600000, 800000]
num_shots = 5

# 遍历所有 CSV 文件
for csv_file in csv_files:
    with open(os.path.join(folder_path, csv_file), 'r') as input_file:
        # 读取 CSV 文件
        csv_reader = csv.reader(input_file)
        # 跳过前 100 行数据
        for _ in range(100):
            next(csv_reader)

        # 创建空列表用于储存筛选后的数据
        filtered_data = [[] for _ in range(num_shots)]

        # 遍历剩余行数的数据
        for row in csv_reader:
            # 如果该行数据不足 5 个，则跳过此行数据
            if len(row) < 5:
                continue
            # 将第一列数据乘以 1e6，并将第二、第三列数据乘以相应的系数
            new_row = [
                float(row[0]) * 1e6,
                float(row[1]) * 98.96367279,
                row[2],
                row[3],
                float(row[4]) * 1e3
            ]
            # 根据时间范围将数据添加到相应的列表中
            for i, offset in enumerate(time_offsets):
                if (i * 200000 -500) <= new_row[0] <= (i * 200000 + 1000 ):
                    new_row[0] -= offset
                    filtered_data[i].append(new_row)
                    break

    # 将每个发射次数的数据写入单独的 CSV 文件
    for i, offset in enumerate(time_offsets):
        shot_num = i + 1
        output_file_path = os.path.join(output_folder, f"{csv_file.split('.csv')[0]}_shot{shot_num}.csv")
        with open(output_file_path, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            # 写入表头
            csv_writer.writerow(['Time', 'Current', 'Photodiode1', 'Photodiode2', 'Voltage'])
            # 写入数据
            for row in filtered_data[i]:
                csv_writer.writerow(row)

print("Done!")