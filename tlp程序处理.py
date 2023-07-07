import numpy as np
import csv
import math
import os

# 定义参数


# 定义一个函数
def calculate_Y(a, b, c, d, T):
    y = (2*a + b)/(a + 2*b) - (1 - np.exp(-c/T))/(1-np.exp(-d/T))
    return y

def solve_y(a, b, c, d, max_iter):


    left = 0.1
    right = 100.0

    y_left = calculate_Y(a, b, c, d, left)
    y_right = calculate_Y(a, b, c, d, right)
    if np.abs(y_left) <=  1e-6:
        return left

    elif np.abs(y_right) <= 1e-6:
        return right

    elif np.sign(y_left) == np.sign(y_right):
        print("左右边界符号相同.")

        return None

    elif np.sign(y_left) != np.sign(y_right):
        for _ in range(max_iter):
            mid = (left + right) / 2
            y_mid = calculate_Y(a, b, c, d,  mid)

            if np.abs(y_mid) <=  1e-6 :
                return mid

            elif np.sign(y_mid) == np.sign(y_left):
                left = mid

            elif np.sign(y_mid) == np.sign(y_right):
                right = mid

        return (left + right) / 2

#  定义文件夹
folder_path = r'C:\Users\shangu\Desktop\三探针\test\已处理'  # 文件夹路径
output_folder = r'C:\Users\shangu\Desktop\三探针\test\已处理\已处理'  # 输出文件夹路径
if not os.path.exists(output_folder):-
    os.mkdir(output_folder)

# 获取指定文件夹内所有 csv 文件的文件名
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 遍历 csv 文件并处理
for csv_file in csv_files:
    with open(os.path.join(folder_path, csv_file), 'r') as input_file:
        # 读取 csv 文件
        csv_reader = csv.reader(input_file)

        # 创建空列表用于储存筛选后的数据
        filtered_data_1 = []
        # 遍历剩余行数的数据

        for row in csv_reader:
                try:
                    i_2 = float(row[2])
                    i_3 = float(row[1])
                    v_2 = float(row[4])
                    v_3 = float(row[3])
                    dd = 15
                    solution = solve_y(i_2, i_3, v_2, v_3, dd)
                    if solution * 3 >= float(row[4]):

                        try:
                            e_den = 0.53 * 10**(12) * (i_3 - i_2*np.exp((v_2 - v_3) / solution) * (1-np.exp((v_2-v_3)/solution))) ** (-1) * (1.6 * 10**(-19) / solution )**(-0.5)
                        except:
                            print('电子密度错误')
                            pass
                    else:
                        solution = v_2 / math.log((-i_2 - 2*i_3) / (i_2 - i_3))
                        e_den = i_3 * 0.53 * 10**(12) * (1.6 * 10**(-19) / solution )**(-0.5)


                    new_row = [ float(row[0]), solution, e_den ]
                    # 添加处理后的数据到 filtered_data_1 列表中
                    filtered_data_1.append(new_row)
                except:
                    print('数据不对')
                    pass
        with open(os.path.join(output_folder, csv_file.split('.csv')[0] + '_processed.csv'), 'w', newline='') as output_file_1:
            csv_writer_1 = csv.writer(output_file_1)
            csv_writer_1.writerow(['Time', 'Electron Temperature', 'Electron Density'])
            for row in filtered_data_1:
                csv_writer_1.writerow(row)

print('done')
