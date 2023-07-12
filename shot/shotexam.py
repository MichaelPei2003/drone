import math
from dronekit import LocationGlobal, VehicleMode
from send_body_ned_velocity import send_body_ned_velocity
import cv2
import numpy as np
import socket
import time
import pigpio
def shotexam(vehicle):
    # 初始化PID控制器
    dt=0.1
    kp = 0.005  # 比例参数
    ki = 0.0001  # 积分参数
    kd = 0.0001  # 微分参数
    error_x = 0
    error_y = 0
    proportional_x=0
    proportional_y=0
    integral_x = 0
    integral_y = 0
    derivative_x=0
    derivative_y=0
    last_error_x = 0
    last_error_y = 0


    target_location_x = 0 #晚点再设置吧
    target_location_y = 0
    

        
    # 获取当前位置
    current_location_x=3200
    current_location_y=2400


    # 计算误差
    error_x = -(target_location_x - current_location_x)
    error_y = -(target_location_y - current_location_y)

    # 计算PID控制信号
    proportional_x = error_x
    proportional_y = error_y
    integral_x += error_x*dt
    integral_y += error_y*dt
    derivative_x = error_x - last_error_x
    derivative_y = error_y - last_error_y
    last_error_x = error_x
    last_error_y = error_y

    vx = kp * proportional_x + ki * integral_x + kd * derivative_x
    vy = kp * proportional_y + ki * integral_y + kd * derivative_y
    print("speed:")
    print("vx:",vx,"vy:",vy)
    # 发送控制信号
    send_body_ned_velocity(vy, vx, 0,vehicle)

    # 检查是否到达目标点
    if abs(error_x) < 1 and abs(error_y) < 1:
        print("Reached target location")
        

