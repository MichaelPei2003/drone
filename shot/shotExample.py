#from multiprocessing import connection
import time
#from dronekit import LocationGlobal, VehicleMode
from send_body_ned_velocity import send_body_ned_velocity
import cv2
import numpy as np
import socket
import time

# coord_str="0,0"
# if coord_str != '0':
#     tx, ty = coord_str.split(",")
#     print("(",tx,",",ty,")")

def shot(vehicle):
    # 初始化PID控制器
    dt = 0.1
    kp = 0.2  # 比例参数
    ki = 0.1  # 积分参数
    kd = 0.5  # 微分参数
    integral = 0
    last_error = 0

    while True:
        #接收数据
        coord_str="0,0"
        if coord_str != '0':
            tx, ty = coord_str.split(",")
            print("(",tx,",",ty,")")

            # 设置目标点
            ### !!! 摄像头的坐标误差
            target_location=(tx,ty,2.5)#晚点再设置吧
        else:
            print(0)

    

        # 控制循环
        while True:
            # 获取当前位置
            lx=320
            ly=240
            current_location = (lx,ly,2.5)

            # 计算误差
            error = target_location - current_location

            # 计算PID控制信号
            proportional = error
            integral += error*dt
            derivative = (error - last_error)/dt
            last_error = error

            vx = kp * proportional.lat + ki * integral.lat + kd * derivative.lat
            vy = kp * proportional.lon + ki * integral.lon + kd * derivative.lon
            vz = kp * proportional.alt + ki * integral.alt + kd * derivative.alt

            # 发送控制信号
            send_body_ned_velocity(vx, vy, vz, dt,vehicle)

            # 检查是否到达目标点
            if error.lat < 0.001 and error.lon < 0.001 and error.alt < 0.1:
                print("Reached target location")
                break

            # 等待一段时间
            time.sleep(0.1)

