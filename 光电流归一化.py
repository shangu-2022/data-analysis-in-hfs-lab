import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# 定义要处理的文件夹路径
folder_path = r'D:\03  实验数据\正式实验\电压电流光电流\十路\20230703\110Pa'  # 待处理文件夹路径
#output_folder = r'D:\03  实验数据\test\pd_processed'  # 输出文件夹路径

# 获取文件夹中的所有次级文件夹
subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

# 遍历每个次级文件夹并处理其中的文件
for subfolder in subfolders:
    output_folder = os.path.join(subfolder, 'pd_normalized_processed')
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    # 获取次级文件夹中的所有文件
    files = [f.path for f in os.scandir(subfolder) if f.is_file()]

    # 在这里进行您的文件处理操作
    for file in files:
        # 处理文件的代码
        with open(file, 'r') as input_file:
            df = pd.read_csv(file)
            time = df.iloc[:, 0].astype(float)
            current = df.iloc[:, 1].astype(float)
            pd1 = df.iloc[:, 2].astype(float)
            pd2 = df.iloc[:, 3].astype(float)
            voltage = df.iloc[:, 4].astype(float)
            # 第二步：计算平均幅值并减去平均值
            pd1_average = np.mean(pd1[:1000])
            pd2_average = np.mean(pd2[:1000])
            pd1 -= pd1_average
            pd2 -= pd2_average
            # 开始归一化
            pd1_peak_value = np.max(pd1)
            pd2_peak_value = np.max(pd2)
            pd1_peak_value_index = np.where(pd1 == pd1_peak_value)[0]
            pd2_peak_value_index = np.where(pd2 == pd2_peak_value)[0]
            # pd1_values = []
            # pd1_indexs = []
            # pd2_values = []
            # pd2_indexs = []
            # pd1_normalized =pd.Series(pd1_values , index= pd1_indexs)
            # pd2_normalized = pd.Series(pd2_values, index=pd2_indexs)
            # for i in pd1.index:
            #     pd1_value = pd1[i]  / pd1_peak_value
            #     pd2_value = pd2[i] / pd2_peak_value
            #     pd1_normalized[i] = pd1_value
            #     pd2_normalized[i] = pd2_value
            pd1_normalized = pd1 / pd1_peak_value
            pd2_normalized = pd2 / pd2_peak_value
            # 替换原始 DataFrame 中的 pd1 列
            df['Photodiode1'] = pd1_normalized
            df['Photodiode2'] = pd2_normalized


        filename = os.path.basename(file)
        output_file = os.path.join(output_folder, filename)
        df.to_csv(output_file, index=False)


print('done!')
