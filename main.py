import cv2
import numpy as np
import socket
import time
from find import find,pid_move
from dronekit import connect, VehicleMode
import time
from RTL import PidRTL
from scout import scout
from send_body_ned_velocity_notime import send_body_ned_velocity_notime
from send_body_ned_velocity import send_body_ned_velocity
from threading import Thread
from index import _init,get_value,set_value
from get_target_location import get_target_location
from pymavlink import mavutil
from yolo import yolo
from heading import set_heading
from alt_hold import alt_hold

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string)
vehicle = connect (connection_string, wait_ready = True) 

_init()
k=0.002#控制vx和vy
# 初始化PID控制器
dt=0.5
kp = 0.5  # 比例参数
ki = 0.1  # 积分参数
kd = 0.18  # 微分参数
max_vx=0.4 #前后方向最大速度
max_vy=0.4 #左右方向最大速度
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
target_location_x=0
target_location_y=0
allow_error_x=50
allow_error_y=50
count_in_circle = 40
count_in_circle_now = 0

F_servo = 0
set_value(4,F_servo)


time0 = time.time()
print((time.time()-time0))

#get scout area start
scout_start = get_target_location(-2, 53, vehicle)
print("scout start: lat: ", scout_start.lat, " lon: ", scout_start.lon)


#takeoff and leave tekeoff area
default_heading = vehicle.heading
print("current location: lat: ", vehicle.location.global_frame.lat, "lon: ", vehicle.location.global_frame.lon)
shot_start = get_target_location(0, 30, vehicle)
print("shot start: lat: ", shot_start.lat, "lon: ", shot_start.lon)
daemon_thread = Thread(target=yolo)
daemon_thread.daemon = True  # 设置线程为守护线程

# 启动守护线程
daemon_thread.start()
time.sleep(5)

print("Arming motors...")
vehicle.mode = VehicleMode("GUIDED")
print("Vehicle mode: GUIDED")
vehicle.armed = True
print("Vehicle armed")
#if not armed do following loop
while not vehicle.armed:
    print("Waiting for arming...")
    time.sleep(1)
vehicle.mode = VehicleMode("GUIDED")

time0 = time.time()
print((time.time()-time0))

print("Taking off")
vehicle.simple_takeoff(6)
time.sleep(12)
"""
for i in range(30):
    vehicle.simple_goto(shot_start, airspeed = 1)
    time.sleep(1)
    print(vehicle._rngfnd_distance)
    if vehicle._rngfnd_distance > 5.5:
        send_body_ned_velocity_notime(0, 0, 0.3, vehicle)
        time.sleep(1)
    elif vehicle._rngfnd_distance < 4.5:
        send_body_ned_velocity_notime(0, 0, -0.3, vehicle)
        time.sleep(1)
"""

vehicle.simple_goto(shot_start, airspeed = 1)
for i in range(25):
    print(vehicle._rngfnd_distance)
    time.sleep(1)

shot_start.alt = vehicle.location.global_frame.alt - 1

vehicle.simple_goto(shot_start, airspeed = 0.6)
time.sleep(5)

vehicle.simple_goto(shot_start, airspeed = 0.3)
time.sleep(5)

alt_hold(4, vehicle)
#side,l用于find
"""
l控制无人机飞行的速度
f和side共同控制无人机飞行的方向
"""
side = 1
Tfind = 3
f = 1

flag_changeside = 1
flag_changef = 0

zero=20
figet=0


# run_servo = 0v
# flag
fshot = 0
f_reach_shot = 1
fscout = 0
f_goto_scout = 0
print((time.time() - time0))


# 以下时间用于find绕圈的时间计数
time_findstart = 0
count_t = 0
timeForFind = 0

# 以下时间用于shot超时的计数
time_findstart = time.time()
time_shotstart = time_findstart

print("开始投弹部分")
while True:
    # 接收数据coord_str
    flag_servo=get_value(0)
    x=get_value(2)
    y=get_value(3)
    if x != 0 and y != 0:
        # 在前进的过程中识别到桶则直接跳出simple_goto
        """
        if f_reach_shot == 0:
            vehicle.commands.upload()
            set_heading(vehicle, default_heading)
            time_findstart = time.time()
            time_shotstart = time_findstart
            f_reach_shot = 1
            print("识别到桶, shot reached")
            alt_hold(4, vehicle)
        """
        # print("(", x, ",", y, ")", flag_servo)
        if flag_servo == 1:
            send_body_ned_velocity(0, 0, 0, 5,vehicle)
            print("Reached target location")
            # wait to move
            break
        # 识别到后重置find中的side和Tfind
        side = 1
        Tfind = 3
        f = 1
        flag_changeside = 1
        flag_changef = 0

        target_location_x = int(x)  # 图传返回的圆筒坐标，是目标点的坐标
        target_location_y = int(y)
        if time.time()-time_shotstart > 60:
            print("time>60无法找到目标，放弃，直接投弹")
            F_servo=1
            set_value(4,F_servo)
            break
        pid_move(vehicle, target_location_x, target_location_y)
    elif x == 0 and y == 0 and f_reach_shot != 0:
        # 以下时间用于find绕圈的时间计数
        timeForFind = time.time()
        count_t = timeForFind - time_findstart
        print("count_t // Tfind=",count_t // Tfind)
        if count_t // Tfind == 0:
            if flag_changeside == 1:#改变side、改变两个flag
                side = side % 2 + 1
                flag_changeside=0
                flag_changef=1
                if side == 2 and f == 1:
                    print("vehicle向前行进",Tfind,"秒")
                elif side == 2 and f == -1:
                    print("vehicle向后行进",Tfind,"秒")
            find(vehicle, 4, side, f)
    
        elif Tfind >= 11:
            print("Tfind>=11无法找到目标，放弃，直接投弹")
            F_servo=1
            set_value(4,F_servo)
            break
        elif count_t // Tfind == 1:  #改变side和f，改变两个flag
            if flag_changef==1:
                side = side % 2 + 1
                f=-f
                flag_changeside=1
                flag_changef=0
                if side == 1 and f == -1:
                    print("vehicle向右行进",Tfind,"秒")
                elif side == 1 and f == 1:
                    print("vehicle向左行进",Tfind,"秒")
    
            find(vehicle, 4, side, -f)
    
        else: #增加绕圈时间，重置time_findstart
            Tfind=Tfind+2
            time_findstart=time.time()
        continue
    
    # 完全离开起飞区域后倒计时12秒，若超时则直接切入shot
    """
    elif x == 0 and y == 0 and f_reach_shot == 0 and time.time() - time_start <= 12:
        print("尚未识别到桶，继续前进")
        continue
    
    elif x == 0 and y == 0 and f_reach_shot == 0 and time.time() - time_start > 12:
        print("计时结束，shot reached")
        set_heading(vehicle, default_heading)
        time_findstart = time.time()
        time_shotstart = time_findstart
        f_reach_shot = 1
        alt_hold(4, vehicle)
    """
#        # 检查是否到达目标点
#        if abs(error_x) < allow_error_x and abs(error_y) < allow_error_y:
#            count_in_circle_now = count_in_circle_now + 1
#            if int(flag_servo)==1:
#                print("Reached target location")
#                pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
#                # time.sleep(1)
#                run_servo = 1
#                print("投弹完成，请继续执行")
#                fshot=1
#                #wait to move
#                break
#            if vehicle.location.global_relative_frame.alt>=4:
#                send_body_ned_velocity_notime(0,0,0.05,vehicle)
#        else:
#            count_in_circle_now=0

print((time.time()-time0))
#from shot area to scout area
"""
vehicle.simple_goto(scout_start, airspeed = 1.5)
time.sleep(17)
print("go to scout")
set_heading(vehicle,default_heading)
alt_hold(4, vehicle)
time.sleep(2)
print("move over")
"""
#model scout
#velocity_z is unused in send_body_ned_velocity
"""
print("scout open!")
send_body_ned_velocity(1, 0, 0, 2, vehicle)
set_heading(vehicle,default_heading)
print("Heading corrected !")
print("first path")
time.sleep(1)

send_body_ned_velocity(-1,1.25,0,2,vehicle)
set_heading(vehicle,default_heading)
print("Heading corrected !")
print("second path")
time.sleep(1)

send_body_ned_velocity(1,0,0,2,vehicle)
set_heading(vehicle,default_heading)
print("Heading corrected !")
print("third path")
time.sleep(1)

send_body_ned_velocity(-1,1.25,0,2,vehicle)
set_heading(vehicle,default_heading)
print("Heading corrected !")
print("forth path")
time.sleep(1)

send_body_ned_velocity(1,0,0,2,vehicle)
set_heading(vehicle,default_heading)
print("Heading corrected !")
print("fifth path")
time.sleep(1)

send_body_ned_velocity(-0.5,-1.25,0,4,vehicle)
set_heading(vehicle,default_heading)
print("Heading corrected !")
print("sixth path")
time.sleep(1)

print("end scouting.")
print((time.time()-time0))
"""
#model RTL      
print("RTL open!")
vehicle.mode = VehicleMode("RTL")
time.sleep(10)
print("gogogo")
vehicle.mode = VehicleMode("GUIDED")
alt_hold(4,vehicle)
frtl=0
set_value(1,frtl)
while True:
    x=get_value(2)
    y=get_value(3)
    if x!=0 and y!=0: 
        dx=x
        dy=y
        PidRTL(dx,dy,frtl,vehicle)
        frtl=get_value(1)
    elif time.time()-time0>290:
        vehicle.mode = VehicleMode("LAND")
        time.sleep(10)
        vehicle.armed = False
        break
print((time.time()-time0))

