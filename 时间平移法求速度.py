import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
data = pd.read_csv(r'D:\03  实验数据\绝缘件对等离子体参数的影响\绝缘件二\光电流\test\数据预处理\tek0000_shot1.csv')

# 获取各列数据
time = data.iloc[:, 0].astype(float)
print(time)
current = data.iloc[:, 1].astype(float)
pd1 = data.iloc[:, 2].astype(float)
pd2 = data.iloc[:, 3].astype(float)
voltage = data.iloc[:, 4].astype(float)

# 第二步：计算平均幅值并减去平均值
pd1_average = np.mean(pd1[:1000])
pd2_average = np.mean(pd2[:1000])
pd1 -= pd1_average
pd2 -= pd2_average

# 第三步：归一化数据点
time_range_indices = np.where((time >20) & (time < 60))[0]
print(time_range_indices)
pd1_range = pd1[time_range_indices]
print(pd1_range)
pd2_range = pd2[time_range_indices]
print(pd2_range)
time_total = time[time_range_indices]


pd1_peak_value = np.max(pd1_range)

pd2_peak_value = np.max(pd2_range)
print(pd1_peak_value)
print(pd2_peak_value)
normalized_pd1 = (pd1 - np.min(pd1_range)) / (pd1_peak_value - np.min(pd1))
normalized_pd2 = (pd2 - np.min(pd2)) / (pd2_peak_value - np.min(pd2))

# 第四步：并筛选百分之十到百分之九十的数据点
pd1_peak_index = np.argmax(pd1)  # 找到 pd1 峰值索引
pd1_lower_bound = pd1_peak_value * 0.2  # 百分之十的下界
pd1_upper_bound = pd1_peak_value * 0.8  # 百分之九十的上界
time_range1 = np.where(time < time[pd1_peak_index])[0]
pd1_values = pd1[time_range1][(pd1[time_range1] > pd1_lower_bound) & (pd1[time_range1] < pd1_upper_bound)]


pd2_peak_index = np.argmax(pd2)  # 找到 pd2 峰值索引
pd2_lower_bound = pd2_peak_value * 0.2  # 百分之十的下界
pd2_upper_bound = pd2_peak_value * 0.8  # 百分之九十的上界
time_range2 = np.where(time < time[pd2_peak_index])[0]
pd2_values = pd1[time_range2][(pd1[time_range2] > pd1_lower_bound) & (pd1[time_range2] < pd1_upper_bound)]

print(time[pd1_peak_index])
print(time[pd2_peak_index])

# 第五步：寻找时间平移
best_shift = 0
min_error = float('inf')
pd1_indices = np.where((time > 0) & (time < 150))[0]  # 获取 pd1 范围内的索引

for shift in np.arange(0, 20, 0.1):
    shifted_pd2 = pd2.shift(int(shift * 1), fill_value=0)  # 将 shift 转换为整数索引
    error = np.mean((pd1[pd1_indices] - shifted_pd2[pd1_indices]) ** 2)
    if error < min_error:
        min_error = error
        best_shift = shift
print("平移的时间：", best_shift)


# 第六步：画图
pic_normalized_pd1 = normalized_pd1[time_range_indices]
pic_normalized_pd2 = normalized_pd2[time_range_indices]

plt.plot(time_total, pic_normalized_pd1, color='blue', label='Normalized PD1')
plt.plot(time_total, pic_normalized_pd2, color='purple', label='Normalized PD2')
plt.plot(time_total, pic_normalized_pd2.shift(int(best_shift * 100), fill_value=0), color='red', label='Shifted Normalized PD2')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Normalized Current')
plt.show()

print("平移的时间：", best_shift)

