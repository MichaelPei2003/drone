import time

from dronekit import connect, VehicleMode
from pymavlink import mavutil
from send_body_ned_velocity import send_body_ned_velocity
from control_flight import control_flight

import example1

def scout(location, vehicle = None):
    #记录此刻的位置，并停住
    time.sleep(5)
    now_time=time.time()
    now_loc=location
    
    #pid，运行到圆筒的正上方
    
    #此处放pid代码
    while True:
        # 省略了接收实时坐标部分代码，这里假设从视觉接收到的坐标为(0，0)
        x = 0
        y = 0

        # 控制飞行
        control_flight(x, y)
        if speed_x == 0 and speed_y == 0 :
            break

        time.sleep(1)  # 此处为每秒执行一次循环，之后要根据摄像头帧率调整延时

    time.sleep(10)

    #下降到能看清圆筒内容的高度
    send_body_ned_velocity(0, 0, -1, 1)
    time.sleep(10)

    #回到原来的巡航路线上
    
    #依靠经纬度
    vehicle.simple_goto(now_loc)
    time.sleep(5)
    rest_time=duration-(now_time-start_time)
    send_body_ned_velocity(v_x,v_y,0,rest_time)
    
    #依靠相对位置
    send_body_ned_velocity(-ori_x,-ori_y,0,1)
    if cyl == 1 :# 看到圆筒
        scout(loc)
