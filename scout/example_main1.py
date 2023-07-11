import time 
from dronekit import connect,VehicleMode

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.arm_and_takeoff import arm_and_takeoff

from send_body_ned_velocity import send_body_ned_velocity
from send_body_angle import send_body_angle

 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='192.168.159.182:14550' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(5,vehicle)

# cyl = 0    #是否检测到圆筒，初始值为0指未检测到

#路线2
#←↑→

#向左旋转90度
send_body_angle(-90,5,vehicle)
time.sleep(3)
print("turn left 90 degree overed")

#向前运动5m
start_time = time.time()
duration = 5    #运动的持续时间
v_x = 1    #飞机在前后方向上的速度，前为正
v_y = 0    #飞机在左右方向上的速度，右为正
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# if cyl == 1 :    #检测到圆筒
#     scout(v_x,v_y,duration,start_time,vehicle)
time.sleep(5)
print("5m overed")

#向右旋转90度
send_body_angle(90,5,vehicle)
time.sleep(3)
print("turn right 90 degree overed")

#向前运动2m
start_time = time.time()
duration = 2
v_x = 1
v_y = 0
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
time.sleep(5)
print("2m overed")

#向右旋转90度
send_body_angle(90,5,vehicle)
time.sleep(3)
print("turn right 90 degree overed")

#向前运动5m
start_time = time.time()
duration = 5
v_x = 1
v_y = 0
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# if cyl == 1 :
#     scout(v_x,v_y,duration,start_time,vehicle)
time.sleep(5)
print("5m overed")

#调个头
send_body_angle(180,5,vehicle)
time.sleep(3)
print("turn backward")

#向前运动5m
start_time = time.time()
duration = 5    #运动的持续时间
v_x = 1    #飞机在前后方向上的速度，前为正
v_y = 0    #飞机在左右方向上的速度，右为正
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# if cyl == 1 :    #检测到圆筒
#     scout(v_x,v_y,duration,start_time,vehicle)
time.sleep(5)
print("5m overed")

#向左旋转90度
send_body_angle(-90,5,vehicle)
time.sleep(3)
print("turn left 90 degree overed")

#向前运动2m
start_time = time.time()
duration = 2
v_x = 1
v_y = 0
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
time.sleep(5)
print("2m overed")

#向左旋转90度
send_body_angle(-90,5,vehicle)
time.sleep(3)
print("turn left 90 degree overed")

#向前运动5m
start_time = time.time()
duration = 5
v_x = 1
v_y = 0
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# if cyl == 1 :
#     scout(v_x,v_y,duration,start_time,vehicle)
time.sleep(5)
print("5m overed")

vehicle.mode = VehicleMode("RTL")
