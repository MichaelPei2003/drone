from dronekit import connect, VehicleMode
from send_body_ned_velocity import send_body_ned_velocity
import math
import time

from index import set_value
from index import get_value

connection_string = 'udp:127.0.0.1:14550'  
vehicle = connect(connection_string, wait_ready=True)

target_coordinate = (1, 1)  # 目标坐标，即应投弹时视觉检测出的圆筒中心坐标

Kp = 0.5  
Ki = 0.1  
Kd = 0.2  

# 初始化误差和积分误差
error_sum = 0
last_error = 0

def control_flight(x, y):
    global error_sum_x, error_sum_y, last_error_x, last_error_y, speed_x, speed_y

    # 计算坐标差异
    dx = x - target_coordinate[0]
    dy = y - target_coordinate[1]

    # 当目标点在当前点的左侧时，dx 为负值；当目标点在当前点的右侧时，dx 为正值
    # 当目标点在当前点的后方时，dy 为负值；当目标点在当前点的前方时，dy 为正值

    error_x = dx
    error_sum_x += error_x
    error_diff_x = error_x - last_error_x
    speed_x = Kp * error_x + Ki * error_sum_x + Kd * error_diff_x
    t_x = speed_x / error_x

    error_y = dy
    error_sum_y += error_y
    error_diff_y = error_y-last_error_y
    speed_y = Kp * error_y + Ki * error_sum_y + Kd * error_diff_y
    t_y = speed_y / error_y
    
    if t_x < t_y :
        t = t_y
    else :
        t = t_x
    
    send_body_ned_velocity(speed_x,speed_y,0,t)
# 更新上一次的误差
    last_error_x = error_x
    last_error_y = error_y

    set_value(0,speed_x)
    set_value(1,speed_y)


