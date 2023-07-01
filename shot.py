from multiprocessing import connection
import time
from dronekit import connect,LocationGlobal, VehicleMode

# connection_string = 'udp:192.168.1.2:14550' # 替换为您的无人机IP地址和端口号

#图传图像中心点坐标(240,320)

# 连接到飞机
connection_string='/dev/ttyACM0'
vehicle = connect(connection_string, wait_ready=False)
# 设置目标点
### !!! 摄像头的坐标误差
target_location#晚点再设置吧

# 初始化PID控制器
kp = 0.2  # 比例参数
ki = 0.1  # 积分参数
kd = 0.5  # 微分参数
integral = 0
last_error = 0

# 控制循环
while True:
    # 获取当前位置
    current_location = vehicle.location.global_relative_frame

    # 计算误差
    error = target_location - current_location

    # 计算PID控制信号
    proportional = error
    integral += error
    derivative = error - last_error
    last_error = error

    vx = kp * proportional.lat + ki * integral.lat + kd * derivative.lat
    vy = kp * proportional.lon + ki * integral.lon + kd * derivative.lon
    vz = kp * proportional.alt + ki * integral.alt + kd * derivative.alt

    # 发送控制信号
    vehicle.send_body_ned_velocity(vx, vy, vz)

    # 检查是否到达目标点
    if error.lat < 0.00001 and error.lon < 0.00001 and error.alt < 0.1:
        print("Reached target location")
        break

    # 等待一段时间
    time.sleep(0.1)

