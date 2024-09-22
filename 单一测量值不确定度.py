# 需要提前安装numpy库
import numpy as np

# 需要修改的值
# 测量值(输入示例：x = np.array([1，(10+1)**2，114514，203912049.52131]))
x = np.array([])
# 测量仪器误差限/精密度/随机误差大小(自行查表输入)
accuracy = 0.5

# 包含因子的值(一般无需修改)
k = 3 ** (1 / 2)

# 以下内容无需修改
len = x.size
x_ave = x2_ave = delta2 = 0
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
for i in range(0, len):
    delta2 += (x[i] - x_ave) ** 2
# 贝塞尔公式
sx = (delta2 / (len - 1)) ** (1 / 2)
print("标准误差sigma(x)的估计值=有限次测量的标准误差s(x)=", sx)
ua = sx_ave = (delta2 / (len * (len - 1))) ** (1 / 2)
print(
    "不确定度的A类估计Ua(x)=均值的标准(偏)差s(ave_x)= 根号下",
    delta2,
    "/",
    len * (len - 1),
    "=",
    sx_ave,
)
ub = accuracy / k
print("不确定度的B类估计Ub(x)=", ub)
u = (ua**2 + ub**2) ** (1 / 2)
print("不确定度U(x)=", u)
print("最终测量结果ave_x+-U(x)=", x_ave, "+-", u)
