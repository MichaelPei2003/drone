from transfer_scout import transfer
import time 
from dronekit import connect,VehicleMode


import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.arm_and_takeoff import arm_and_takeoff

from threading import Thread

from send_body_ned_velocity import send_body_ned_velocity
from scout.useless.send_body_angle import send_body_angle
from scout import scout
from index import set_value
from index import get_value
from index import _init

 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='172.20.10.6:14550' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(5,vehicle)

# cyl = 0    #是否检测到圆筒，初始值为0指未检测到

# #前往侦查区
# print("start going to scout area ...")
# send_body_ned_velocity(5,1,0,4,vehicle)
# time.sleep(5)
# print("reach scout area")

daemon_thread = Thread(target=transfer)
daemon_thread.daemon = True  # 设置线程为守护线程

# 启动守护线程
daemon_thread.start()

_init()

data=0


#路线2
#←↑→

#向左走7m

duration=7
x_duration=duration*2
for x in range(x_duration):
    v_x=0
    v_y=-1
    send_body_ned_velocity(v_x,v_y,0,0.5,vehicle)
    data = get_value(0)
    if data != 0:
        entry_time=time.time()
    while data != 0 :
        scout(v_x,v_y,vehicle)
        break_time=get_value(1)
        duration=duration-(break_time-entry_time)*0.5
        data = get_value(0)
    x_duration=duration*2
    x_duration=int(x_duration)
time.sleep(5)
print("go left 7m")

# #向前走2m
# send_body_ned_velocity(1,0,0,2,vehicle)
# time.sleep(5)
# print("go forward 2m")

# #向右走7m
# send_body_ned_velocity(0,1,0,7,vehicle)
# time.sleep(5)
# print("go right 7m")

# #重新换个方向走一遍

# #向左走7m
# send_body_ned_velocity(0,-1,0,7,vehicle)
# time.sleep(5)
# print("go left 7m")

# #向后走2m
# send_body_ned_velocity(-1,0,0,2,vehicle)
# time.sleep(5)
# print("go backward 2m")

# #向右走7m
# send_body_ned_velocity(0,1,0,7,vehicle)
# time.sleep(5)
# print("go right 7m")

#*******

# #向左旋转90度
# send_body_angle(-90,5,vehicle)
# time.sleep(3)
# print("turn left 90 degree overed")

# #向前运动5m
# start_time = time.time()
# duration = 5    #运动的持续时间
# v_x = 1    #飞机在前后方向上的速度，前为正
# v_y = 0    #飞机在左右方向上的速度，右为正
# send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# # if cyl == 1 :    #检测到圆筒
# #     scout(v_x,v_y,duration,start_time,vehicle)
# time.sleep(5)
# print("5m overed")

# #向右旋转90度
# send_body_angle(90,5,vehicle)
# time.sleep(3)
# print("turn right 90 degree overed")

# #向前运动2m
# start_time = time.time()
# duration = 2
# v_x = 1
# v_y = 0
# send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# time.sleep(5)
# print("2m overed")

# #向右旋转90度
# send_body_angle(90,5,vehicle)
# time.sleep(3)
# print("turn right 90 degree overed")

# #向前运动5m
# start_time = time.time()
# duration = 5
# v_x = 1
# v_y = 0
# send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# # if cyl == 1 :
# #     scout(v_x,v_y,duration,start_time,vehicle)
# time.sleep(5)
# print("5m overed")

# #调个头
# send_body_angle(180,5,vehicle)
# time.sleep(3)
# print("turn backward")

# #向前运动5m
# start_time = time.time()
# duration = 5    #运动的持续时间
# v_x = 1    #飞机在前后方向上的速度，前为正
# v_y = 0    #飞机在左右方向上的速度，右为正
# send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# # if cyl == 1 :    #检测到圆筒
# #     scout(v_x,v_y,duration,start_time,vehicle)
# time.sleep(5)
# print("5m overed")

# #向左旋转90度
# send_body_angle(-90,5,vehicle)
# time.sleep(3)
# print("turn left 90 degree overed")

# #向前运动2m
# start_time = time.time()
# duration = 2
# v_x = 1
# v_y = 0
# send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# time.sleep(5)
# print("2m overed")

# #向左旋转90度
# send_body_angle(-90,5,vehicle)
# time.sleep(3)
# print("turn left 90 degree overed")

# #向前运动5m
# start_time = time.time()
# duration = 5
# v_x = 1
# v_y = 0
# send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
# # if cyl == 1 :
# #     scout(v_x,v_y,duration,start_time,vehicle)
# time.sleep(5)
# print("5m overed")

vehicle.mode = VehicleMode("RTL")
