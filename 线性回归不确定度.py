# 需要提前安装numpy库
import numpy as np

# 需要修改的值
# 测量值(输入示例：y = np.array([1，(10+1)**2，114514，203912049.52131]))
x = np.array([])
y = np.array([])
# 测量仪器误差限/精密度/随机误差大小(自行查表输入)
accuracy = 0.5

# 包含因子的值(一般无需修改)
k = 3 ** (1 / 2)

# 以下内容无需修改
len = x.size
x_ave = x2_ave = 0
print("数据个数k=", len)
x2 = np.empty(len)
for i in range(0, len):
    x_ave += x[i]
    x2[i] = x[i] ** 2
    x2_ave += x2[i]
x_ave /= len
print("ave_x=", x_ave)
x2_ave /= len
print("ave_x2=", x2_ave)

y_ave = y2_ave = 0
y2 = np.empty(len)
for i in range(0, len):
    y_ave += y[i]
    y2[i] = y[i] ** 2
    y2_ave += y2[i]
y_ave /= len
print("ave_y=", y_ave)
y2_ave /= len
print("ave_y2=", y2_ave)

xy_ave = 0
for i in range(0, len):
    xy_ave += x[i] * y[i]
xy_ave /= len
print("ave_xy=", xy_ave)

b = (xy_ave - x_ave * y_ave) / (x2_ave - x_ave**2)
a = y_ave - b * x_ave
print("a=", a)
print("b=", b)

r = (xy_ave - x_ave * y_ave) / (((x2_ave - x_ave**2) * (y2_ave - y_ave**2)) ** 0.5)
print("r=", r)

delta = 0
for i in range(0, len):
    delta += (y[i] - a - b * x[i]) ** 2
delta /= len


uab = b * (1 / (len - 2) * (1 / r**2 - 1)) ** 0.5
uaa = (x2_ave**0.5) * uab
print("uab=", uab)
print("uaa=", uaa)
