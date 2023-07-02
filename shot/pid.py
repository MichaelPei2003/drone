from re import T
import matplotlib.pyplot as plt
import numpy as np

#设置目标位置
tx=480
ty=640
target_location=(tx,ty,2.5)

# 获取当前位置
lx=0
ly=0
current_location = (lx,ly,2.5)
t=0.0001

trainx=[]
trainy=[]

trainx.append(lx)
trainy.append(ly)

# 初始化PID控制器
kp = 1  # 比例参数
ki = 0.5  # 积分参数
kd = 0.3  # 微分参数
integralx = 0
integraly = 0
integralz = 0

last_errorx = 0
last_errory = 0
last_errorz = 0

# 控制循环
while True:

    # 计算误差
    errorx = target_location[0] - current_location[0]
    errory = target_location[1] - current_location[1]
    errorz = target_location[2] - current_location[2]
    print(errorx,errory,errorz)

    # 计算PID控制信号
    integralx += errorx
    integraly += errory
    integralz += errorz

    derivativex = errorx - last_errorx
    derivativey = errory - last_errory
    derivativez = errorz - last_errorz

    last_errorx = errorx
    last_errory = errory
    last_errorz = errorz

    vx = kp * errorx + ki * integralx + kd * derivativex
    vy = kp * errory + ki * integraly + kd * derivativey
    vz = kp * errorz + ki * integralz + kd * derivativez

    # 发送控制信号
    #vehicle.send_body_ned_velocity(vx, vy, vz)
    lx=lx+vx*t
    ly=ly+vy*t
    current_location=(lx,ly,2.5)
    trainx.append(lx)
    trainy.append(ly)

    # 检查是否到达目标点
    if errorx < 0.001 and errory < 0.001 and errorz < 0.1:
        print("Reached target location")
        break

    # 等待一段时间
    #time.sleep(0.2)




plt.figure(figsize=(8,6))  # 定义图的大小
plt.xlabel("time(s)")     # X轴标签
plt.ylabel("Volt")        # Y轴坐标标签
plt.title("Examplex")      #  曲线图的标题

plt.plot(trainx,label="$loss$")            # 绘制曲线图

#在ipython的交互环境中需要这句话才能显示出来
plt.show()

plt.figure(figsize=(8,6))  # 定义图的大小
plt.xlabel("time(s)")     # X轴标签
plt.ylabel("Volt")        # Y轴坐标标签
plt.title("Exampley")      #  曲线图的标题

plt.plot(trainy,label="$loss$")            # 绘制曲线图

#在ipython的交互环境中需要这句话才能显示出来
plt.show()

