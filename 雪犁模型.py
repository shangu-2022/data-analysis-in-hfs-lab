"""
雪犁模型
"""

# 导包
import numpy as np
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt

# 指定输入和输出文件夹
folder_path = r'D:\03  实验数据\绝缘件对等离子体参数的影响\绝缘件二\光电流\test\数据预处理'  # 待处理文件夹路径
output_folder = r'D:\03  实验数据\绝缘件对等离子体参数的影响\绝缘件二\光电流\test\数据预处理\snow_processed'  # 输出文件夹路径
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# 获取指定文件夹内所有 csv 文件的文件名
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 填数值

# 读取数据
for csv_file in csv_files:
    with open(os.path.join(folder_path, csv_file), 'r') as input_file:

        df = pd.read_csv(os.path.join(folder_path, csv_file))
        time = df.iloc[:, 0].astype(float)
        current = df.iloc[:, 1].astype(float)
        # 寻找触发零点，将其认为是电流波形的起始点，最终将其标在图中以便检查
        # time_zero_indices = np.where((time >= -0.2) & (time < 0.2))[0]
        # time_zero_values = time[time_zero_indices]
        # time_zero_value = np.min(abs(time_zero_values))
        # time_zero_indice = np.where(time == time_zero_value)
        time_zero_index = np.argmin(np.abs(time))

        time_1 = time_zero_index
        time_2 = time_zero_index + 1
        # time_zero_values = time[time_zero_indices]
        # time_zero_value = np.min(time_zero_value)
        # time_range = np.where(time >= time_zero_value)

        # 数据点漂零
        current_average = np.mean(current[:1000])
        current -= current_average
        # 寻找电流峰值
        current_peak_value = np.max(current)
        current_peak_index = np.where(current == current_peak_value )
        current_peak = pd.Series(current_peak_value,index = current_peak_index)

        # 赋初值
        presure = 15  # 工作气压
        step_size = 0.1 * 1e-6 # 时间步长，单位秒
        e = 1.6 * 1e-19
        m_i = 6.7 * 1e-26
        n_ori = 0.2 * 6.02 * 1e23 / 0.04
        n_sec = n_ori
        area = 3.142 * (4 * 1e-4 - 0.25 * 1e-4)
        mass_density = 1.8 * presure / 1e5
        # 磁压力计算
        force_mag_value = [0]*30000
        force_mag_indice = range(30000)
        force_mag = pd.Series(force_mag_value,index = force_mag_indice)
        for i in current.index:
            if i > time_zero_index:
                force_mag_dot = 1.318 * 1e-7 * current[i] * current[i] * 1e6
                force_mag.loc[i] = force_mag_dot

        # 摩擦力计算
        force_fric_value = [0]*30000
        force_fric_indice = range(30000)
        force_fric = pd.Series(force_fric_value, index=force_fric_indice)
        # 质量计算
        mass_value = [2 * 1e-10]*30000
        mass_indice = range(30000)
        mass = pd.Series(mass_value, index=mass_indice)
        # 速度计算
        velocity_value = [0]*30000
        velocity_indice = range(30000)
        velocity = pd.Series(velocity_value, index=velocity_indice)
        # 加速度计算
        accelerate_value = [0]*30000
        accelerate_indice = range(30000)
        accelerate = pd.Series(accelerate_value, index=accelerate_indice)
        # 位移计算
        displace_value = [0]*30000
        displace_indice = range(30000)
        displace = pd.Series(displace_value, index=displace_indice)
        #赋初值
        # velocity[time_1] = velocity[time_2] = 0
        # accelerate[time_1] = accelerate[time_2] = 0
        # mass[time_1] = mass[time_2] = 2 * 1e-10
        # displace[time_1] = displace[time_2] = 0
        # force_fric[time_1] = force_fric[time_2] = 0
        #进行计算
        for i in current.index:

            if i > time_2:
                accelerate_dot = (force_mag.loc[i-1] - force_fric[i-1] - velocity[i-1] * ((mass[i-1] -mass[i-2])/step_size)) / mass[i-1]
                accelerate.loc[i] = accelerate_dot
                velocity_dot = velocity[i-1] + accelerate[i-1] * step_size
                velocity.loc[i] = velocity_dot
                displace_dot = displace[i-1] + velocity[i-1] * step_size + 0.5 * accelerate[i-1] * step_size * step_size
                displace.loc[i] = displace_dot
                mass.loc[i] = mass[i-1] + area * (displace[i] - displace[i-1]) * mass_density
                force_fric.loc[i] = 0.5 * current[i] * 1e3 * m_i * velocity[i] / e


        # 生成输出文件名
        output_filename = os.path.splitext(csv_file)[0] + '_snow_processed.csv'
        output_path = os.path.join(output_folder, output_filename)

        # 将计算结果保存为CSV文件
        output_df = pd.DataFrame({'Time': time, 'Current': current, 'Force_Mag': force_mag,
                                  'Force_Fric': force_fric, 'Mass': mass, 'Velocity': velocity,
                                  'Accelerate': accelerate, 'Displace': displace})
        output_df.to_csv(output_path, index=False)

        plt.plot(current, color='black', label='current')
        plt.plot(velocity, color='red', label='velocity')
        plt.plot(displace, color='blue', label='pd1_rising_edge')
        # plt.plot(pd2_rising_edge, color='red', label='pd2_rising_edge')
        # plt.plot(pd2_shift_rising_edge, color='purple', label='pd2_shift_series')
        # plt.plot(pd1_peak, color='red', label='pd1_peak', marker='s', markersize=2)
        # plt.plot(pd2_peak, color='blue', label='pd2_peak', marker='s', markersize=2)

        plt.legend()
        plt.xlabel('Index')
        plt.ylabel('Values')
        plt.title('current')
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_file))[0] + '.png')
        plt.savefig(output_file)
        plt.close()

print('down!')






















