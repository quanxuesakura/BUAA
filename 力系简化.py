import numpy as np

ForcesAndPoints = [
    ((0, 0, 100), (0, -15, 0)),
    ((0, 0, -100), (0, 15, 0)),
    ((0, -200, 0), (0, 0, 10)),
    ((0, 200, 0), (0, 0, -10)),
    ((-400, 300, 0), (0, 0, -5)),
    ((400, -300, 0), (0, 0, 5)),
]
moments = []
M, R = np.zeros(3), np.zeros(3)
for force, point in ForcesAndPoints:
    R += force
    moment = np.cross(point, force)
    M += moment
if R.any() != 0:
    r = np.cross(R, M) / np.dot(R, R)
else:
    r = "不存在简化中心"
print(R, M, r)
